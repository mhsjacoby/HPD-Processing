"""
Image_Resize.py
Maggie Jacoby
created 03/22/2020
Updated: 2020-09-21 : Use gen_argparse, change way files are read in and saved. 

This class takes the images that were unpickled to 112x112 size and further 
downsizes them to 32x32 for the public database
"""

import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime
from PIL import Image
import json


from my_functions import *
from gen_argparse import *

class ImageFile():
    def __init__(self, sensor, files_dir, house, write_loc, start_date, img_name, home_system, img_sz=32):
        self.sensor = sensor
        self.original_loc = files_dir   
        self.home = house
        self.system = home_system
        self.img_sz = img_sz
        self.write_path = write_loc
        self.start_date = start_date
        self.img_name = img_name
        self.get_params()  
        self.total_per_day = 86400


    def get_params(self):
        self.path = os.path.join(self.original_loc, self.sensor, self.img_name)

        print(f'getting files from: {self.path}')
        self.write_location = make_storage_directory(os.path.join(self.write_path, self.sensor, f'img-downsized-{self.img_sz}'))
        print(f'resizeing and saving to: {self.write_location}')

    def get_time(self, file_name):
        fname = file_name.split('_')
        day_name, time_name = fname[0], fname[1]
        return day_name, time_name


    def load_image(self, png):
        im = Image.open(png)
        im_array = np.array(list(im.getdata()))
        small_img = im.resize((self.img_sz, self.img_sz), Image.BILINEAR)
        ave_pxl = np.mean(im_array)
        return small_img

    # def write_summary(self, days):
    #     store_dir = make_storage_dicrectory(os.path.join(self.write_path, self.home, self.sensor, 'Summaries'))
    #     fname = os.path.join(store_dir, f'{self.home}-{self.sensor}-img-summary.txt')
    #     with open(fname, 'w+') as writer:
    #         writer.write('hub day %Capt ')
    #         for day in days:
    #             total_captured = self.Day_Summary[day]
    #             try:
    #                 total = total_captured/self.total_per_day
    #                 T_perc = 'f{total:.2}'
    #             except Exception as e:
    #                 print(f'except: {e}')
    #                 T_perc = 0.00
    #             details = f'{self.sensor} {day} {T_perc}'
    #             writer.write(details + '\n')
    #     writer.close()
    #     print(f'{fname}: Write Successful!')
                

    def main(self):
        print(f'Start date: {self.start_date}')
        all_days = sorted(mylistdir(self.path, '2019-', end=False))
        self.Day_Summary = {d:0 for d in all_days}
        print(all_days)

        for day in all_days:
            try:
                if day >= self.start_date:
                    start = datetime.now()
                    F = 0

                    print(day)
                    hours = [str(x).zfill(2) + '00' for x in range(0,24)]
                    all_mins = sorted(mylistdir(os.path.join(self.path, day)))

                    for hr in hours:
                        hr_entry = []
                        this_hr = [x for x in all_mins if x[0:2] == hr[0:2]]
                        if len(this_hr) > 0:
                            for minute in sorted(this_hr):
                                for img_file in sorted(mylistdir(os.path.join(self.path, day, minute))):
                                    day_time = self.get_time(img_file)
                                    str_day, str_time = day_time[0], day_time[1]
                                    if str_day != day:
                                        print(f'day mismatch! file {img_file} is in day {day}')

                                    im_name = f'{str_day}_{str_time}_{self.sensor}_{self.home}.png'     
                                    try:
                                        img_list = self.load_image(os.path.join(self.path, day, minute, img_file))
                                        if img_list != 0:
                                            target_dir = make_storage_directory(os.path.join(self.write_location, str_day, str_time[0:4]))
                                            if not os.path.exists(os.path.join(target_dir, im_name)):
                                                img_list.save(os.path.join(target_dir, im_name))
                                                hr_entry.append(str_time)
                                                self.Day_Summary[day] += 1 


                                    except Exception as e:
                                        print(f'Pillow error: {e}')
                            if len(hr_entry) > 0:
                                print(f'Total entries for {hr} = {len(hr_entry)}')
                                F += len(hr_entry)
                            else:
                                print(f'No images for {day} hour: {hr}')
                        else:
                            print(f'No directories for {day} hour: {hr}')

                    end = datetime.now()
                    print(f'Time to process day {day}: {str(end-start).split(".")[0]}. Number of files: {F}')
            except Exception as e:
                print(f'Error with file {img_file}: {e}')

        # try:
        #     self.write_summary(all_days)
        # except Exception as e:
        #     print(f'Error writing summary: {e}')



if __name__ == '__main__':

    for hub in hubs:
        print(f' hub: {hub}\n stored: {path}\n house: {H_num}\n write: {save_root}\n start: {start_date}')

        I = ImageFile(hub, path, H_num, save_root, start_date, img_name, home_system)
        I.main()
