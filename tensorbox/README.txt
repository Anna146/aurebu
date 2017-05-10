about the general requirements see requirements.txt
about the core tensorbox see tensorbox_readme.md
to download the pre-trained inception model and some demo data run download_data.sh
to train the network run: python train.py --hypes path_to_hype --gpu gpu_number --logdir output_directory
in the hypes/ save the file specifying the datasets and some other network parameters (there is an example)
data/names/reference_dict.txt specifies how the label numbers are translated into human-readable names
to evaluate the trained model run for example: python evaluate.py --weights exit/detect_full_2017_05_01_10.03/save.ckpt-370000 --gpu 0 --test_boxes data/names/val_boxes_valids_good_valids.json
where --weights specify the model