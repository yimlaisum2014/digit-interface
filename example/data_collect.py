import os
import sys
import time

import click

from digit_interface.digit import Digit


class Collect(object):
    def __init__(self):
        # global variable
        self.trial = None
        self.sample = None

        # connect DIGIT
        self.digit_right = Digit("D20356", "Right Gripper")
        self.digit_left = Digit("D20365", "Left Gripper")

        # self.digit_left.connect()
        # self.digit_right.connect()

        self.connect(self.digit_left)
        self.connect(self.digit_right)

        # self.intensity(int(5)) #Under bright env. may not too high

        self.set_camera(self.digit_left)
        self.set_camera(self.digit_right)

        # print("Start collecting")
        # self.collect()

    def connect(self, camera):
        connected = False
        while not connected:
            print('Try connecting....')
            try:
                camera.connect()
                print('Succeed')
                connected = True
            except:
                print('Failed')
                pass
                # import traceback
                # print(traceback.format_exc())
            time.sleep(1)

    def intensity(self, intensity):
        # Maximum value for each channel is 15
        rgb_list = [(intensity, 0, 0), (0, intensity, 0), (0, 0, intensity)]

        for rgb in rgb_list:
            self.digit_left.set_intensity_rgb(*rgb)
            self.digit_right.set_intensity_rgb(*rgb)
            time.sleep(1)
        self.digit_left.set_intensity(intensity)
        self.digit_right.set_intensity(intensity)
        time.sleep(1)

    def set_camera(self, camera):

        intensity = (15, 0, 0)
        if camera is not None:
            camera.set_intensity_rgb(*intensity)
            # set resolution
            camera.set_resolution(Digit.STREAMS['VGA'])
            # set fps
            camera.set_fps(15)

    def disconnect(self):
        self.digit_left.disconnect()
        self.digit_right.disconnect()

    def collect(self):
        # print(sys.argv)
        # print(type(sys.argv[1]))
        self.trial = int(sys.argv[1])
        self.samples = int(sys.argv[2])
        print(type(self.trial), type(self.samples))

        # whether having parmeters
        if self.trial == None or self.samples == None:
            raise Exception("There are missing parmeters -trial -sample) ")

        # make a directionay
        savepath = "Data_2/_60/trial_" + str(self.trial) + "/"
        if not os.path.exists(savepath):
            os.makedirs(savepath)

        # saving images
        for i in range(1, self.samples + 1):
            self.digit_left.save_frame(path=savepath + "left_{}.png".format(i))
            self.digit_right.save_frame(path=savepath + "right_{}.png".format(i))

        print("Finish collecting")
        self.disconnect()


@click.command(help='Collect images')
@click.option('-t', '--trial', required=True, type=click.STRING, help='trial name')
@click.option('-s', '--samples', required=True, type=click.INT, help='Number of samples')
@click.option('-i', '--ignore', required=False, type=click.INT, default=0, show_default=True,
              help='Ignore first n images')
@click.option('-o', '--output', required=True, type=click.Path(file_okay=False, dir_okay=True), help='Output folder')
def collect(trial, samples, ignore, output):
    c = Collect()
    output = os.path.join(output, trial)
    if not os.path.exists(output):
        os.makedirs(output)

    while ignore:
        c.digit_left.get_frame()
        c.digit_right.get_frame()
        ignore -= 1

    with click.progressbar(range(1, samples + 1), length=samples) as bar:
        for idx in bar:
            left = f'left_{idx}.png'
            right = f'right_{idx}.png'
            c.digit_left.save_frame(path=os.path.join(output, left))
            c.digit_right.save_frame(path=os.path.join(output, right))
            idx += 1

    c.disconnect()


if __name__ == "__main__":
    #
    # if (len(sys.argv) < 3):
    #     print('Usage: python data_collect.py trial sample')
    #     sys.exit(1)
    #
    # collect = Collect()
    collect()
