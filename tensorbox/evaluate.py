import tensorflow as tf
import os
import json
import subprocess
from scipy.misc import imread, imresize
from scipy import misc
import numpy as np
import time

from train import build_forward
from utils.annolist import AnnotationLib as al
from utils.train_utils import add_rectangles, rescale_boxes, add_rectangles_big, add_rectangles_plain

import cv2
import argparse

def get_image_dir(args):
    weights_iteration = int(args.weights.split('-')[-1])
    expname = '_' + args.expname if args.expname else ''
    image_dir = '%s/images_%s_%d%s_%f' % (os.path.dirname(args.weights), os.path.basename(args.test_boxes)[:-5], weights_iteration, expname, args.tau)
    return image_dir

def get_results(args, H):
    tf.reset_default_graph()
    x_in = tf.placeholder(tf.float32, name='x_in', shape=[H['image_height'], H['image_width'], 3])
    if H['use_rezoom']:
        pred_boxes, pred_logits, pred_confidences, pred_confs_deltas, pred_boxes_deltas = build_forward(H, tf.expand_dims(x_in, 0), 'test', reuse=None)
        grid_area = H['grid_height'] * H['grid_width']
        pred_confidences = tf.reshape(tf.nn.softmax(tf.reshape(pred_confs_deltas, [grid_area * H['rnn_len'], 2])), [grid_area, H['rnn_len'], 2])
        if H['reregress']:
            pred_boxes = pred_boxes + pred_boxes_deltas
    else:
        pred_boxes, pred_logits, pred_confidences = build_forward(H, tf.expand_dims(x_in, 0), 'test', reuse=None)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, args.weights)

        pred_annolist = al.AnnoList()

        true_annolist = al.parse(args.test_boxes)
        data_dir = os.path.dirname(args.test_boxes)
        image_dir = get_image_dir(args)
        subprocess.call('mkdir -p %s' % image_dir, shell=True)
        all_time = 0
        for i in range(len(true_annolist)):
            true_anno = true_annolist[i]
            orig_img = imread('%s/%s' % (data_dir, true_anno.imageName), mode = 'RGB')[:,:,:3]
            img = imresize(orig_img, (H["image_height"], H["image_width"]), interp='cubic')
            feed = {x_in: img}
            start = time.time()
            (np_pred_boxes, np_pred_confidences) = sess.run([pred_boxes, pred_confidences], feed_dict=feed)
            end = time.time()
            all_time += (end-start)
            #tru_confs = tf.reshape(tf.reduce_max(pred_confidences, reduction_indices=[1,2]),[-1])
            #spred_boxes = tf.reshape(tf.slice(pred_boxes, [0,0,0], [-1,1,4]),[-1,4])
            #mos = tf.fill([], 20)
            #nms = tf.image.non_max_suppression(boxes = spred_boxes, scores = tru_confs, max_output_size = mos)
            #idexes = sess.run(nms, feed_dict=feed)
            #np_pred_boxes = np.array([x[1] for x in enumerate(np_pred_boxes) if x[0] in idexes])
            #np_pred_confidences = np.array([x[1] for x in enumerate(np_pred_confidences) if x[0] in idexes])
            #print(np_pred_boxes.shape)
            
            pred_anno = al.Annotation()
            pred_anno.imageName = true_anno.imageName
            if H['img_out'] == 'norm':
                true_anno = rescale_boxes((orig_img.shape[0], orig_img.shape[1]), true_anno, H["image_height"], H["image_width"])
                new_img, rects = add_rectangles(true_anno.rects, H, [img], np_pred_confidences, np_pred_boxes,
                                            use_stitching=True, rnn_len=H['rnn_len'], tau=args.tau)#, min_conf=args.min_conf, , show_suppressed=args.show_suppressed)
                true_anno = rescale_boxes((H["image_height"], H["image_width"]), true_anno, orig_img.shape[0], orig_img.shape[1])
                imname = '%s/%s' % (image_dir, os.path.basename(true_anno.imageName)[:-4] + '.jpg')
                misc.imsave(imname, new_img)
                misc.imsave('/home/anna/server/imgs/%s' % os.path.basename(true_anno.imageName)[:-4] + '.jpg', new_img)
            if H['img_out'] == 'plain':
                new_img, rects = add_rectangles_plain(true_anno.rects, H, [img], np_pred_confidences, np_pred_boxes,
                                            use_stitching=True, rnn_len=H['rnn_len'], tau=args.tau)
            if H['img_out'] == 'big':
                new_img, rects = add_rectangles_big(true_anno.rects, H, [orig_img], np_pred_confidences, np_pred_boxes,
                                            use_stitching=True, rnn_len=H['rnn_len'])
                imname = '%s/%s' % (image_dir, os.path.basename(true_anno.imageName)[:-4] + '.jpg')
                misc.imsave(imname, new_img)
                                            
                                            
            pred_anno.rects = rects
            pred_anno.imagePath = os.path.abspath(data_dir)
            pred_anno = rescale_boxes((H["image_height"], H["image_width"]), pred_anno, orig_img.shape[0], orig_img.shape[1])
            pred_annolist.append(pred_anno)
            
            if i % 25 == 0:
                print(i)
                print('TIME: ' + str(all_time))
                all_time = 0
    return pred_annolist, true_annolist

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', required=True)
    parser.add_argument('--expname', default='')
    parser.add_argument('--test_boxes', required=True)
    parser.add_argument('--gpu', default=0)
    parser.add_argument('--logdir', default='output')
    parser.add_argument('--iou_threshold', default=0.5, type=float)
    parser.add_argument('--tau', default=0.25, type=float)
    parser.add_argument('--min_conf', default=0.2, type=float)
    parser.add_argument('--show_suppressed', default=True, type=bool)
    parser.add_argument('--img_out', default='norm')
    parser.add_argument('--prec_file', default='someprecision.txt')
    parser.add_argument('--lambda0', default=0.8, type=float)
    parser.add_argument('--lambda1', default=0.2, type=float)
    parser.add_argument('--classID', default=-1, type=int)
    parser.add_argument('--iou', default=None, type=float)
    parser.add_argument('--ignore_classes', default=None, type=bool)
    args = parser.parse_args()
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)
    hypes_file = '%s/hypes.json' % os.path.dirname(args.weights)
    with open(hypes_file, 'r') as f:
        H = json.load(f)
    H['img_out'] = args.img_out 
    H['iou'] = args.iou
    expname = args.expname + '_' if args.expname else ''
    pred_boxes = '%s.%s%s' % (args.weights, expname, os.path.basename(args.test_boxes))
    true_boxes = '%s.gt_%s%s' % (args.weights, expname, os.path.basename(args.test_boxes))
    for_server = '/home/anna/server/model/%s' % (os.path.basename(args.test_boxes))
    
    if args.prec_file is None:
        with open(args.prec_file, 'w') as _: 
            pass
    lambdas = [args.lambda0, args.lambda1]

    pred_annolist, true_annolist = get_results(args, H)
    pred_annolist.save(pred_boxes)
    pred_annolist.save(for_server)
    true_annolist.save(true_boxes)
    
    try:
        if args.ignore_classes:
            rpc_cmd = './utils/annolist/doRPC.py --class %d --minOverlap %f --lambda0 %f --lambda1 %f --prec_file %s --ignore_classes %s %s' % (args.classID, args.iou_threshold, lambdas[0], lambdas[1], args.prec_file, true_boxes, pred_boxes)
        else:
            rpc_cmd = './utils/annolist/doRPC.py --class %d --minOverlap %f --lambda0 %f --lambda1 %f --prec_file %s %s %s' % (args.classID, args.iou_threshold, lambdas[0], lambdas[1], args.prec_file, true_boxes, pred_boxes)
        print('$ %s' % rpc_cmd)
        rpc_output = subprocess.check_output(rpc_cmd, shell=True)
        print(rpc_output)
        txt_file = [line for line in rpc_output.split('\n') if line.strip()][-1]
        output_png = '%s/results.png' % get_image_dir(args)
        plot_cmd = './utils/annolist/plotSimple.py %s --output %s' % (txt_file, output_png)
        print('$ %s' % plot_cmd)
        plot_output = subprocess.check_output(plot_cmd, shell=True)
        print('output results at: %s' % plot_output)
    except Exception as e:
        print(e)
    
if __name__ == '__main__':
    main()
