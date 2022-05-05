import cv2
import os
import matplotlib.pyplot as plt
import pandas as pd

class Process():
    def __init__(self):
        # Before
        self.source_data_path = "Data/"
        self.class_path = "_60/"
        self.trial_loc = self.source_data_path + self.class_path
        # After
        self.type = "add" #(vertical / horizontal / add)
        self.processed_data_path = "Processed_Data/" + self.class_path + self.type + "/"
        
        if not os.path.exists(self.processed_data_path ):
            os.makedirs(self.processed_data_path )

        print("Processing")
        self.process()
        
    
    def process(self):

        
        for t in os.listdir(self.trial_loc):
            sample_loc = self.source_data_path + self.class_path + t
            sample_list_len = float(len(os.listdir(sample_loc)))//2
            sample_list_len = int(sample_list_len)

            for s in range(1,sample_list_len):
                fil_loc_1 = sample_loc + "/left_{}".format(s)+".png"
                fil_loc_2 = sample_loc + "/right_{}".format(s)+".png"
   
        
                #### Read
                img1 = cv2.imread(fil_loc_1)
                img2 = cv2.imread(fil_loc_2)
                
                #### Process (vertical / horizontal / add)
                #v_img = cv2.vconcat([img1,img2])
                if (self.type == "horizontal"):
                    h_img = cv2.hconcat([img1,img2])
                    # Save
                    self.save(t,s,h_img)

                elif (self.type == "add"):
                    a_img = cv2.addWeighted(img1, 1, img2, 1, 0.0)
                    # Save
                    self.save(t,s,a_img)
                else:
                    raise Exception("lack of process type")
                #### Show by opencv
                #cv2.imshow('h_img',h_img)
                #cv2.waitKey(0)
                



        print("Finish Process: total samples is {}".format(len(os.listdir(self.processed_data_path))))
            

    def save(self,trials,samples,processed_img):

        saved_path = self.processed_data_path
        #print(trials)
        #print(samples)
        filename = saved_path + "processed_img_{}_{}.png".format(trials,samples)
        cv2.imwrite(filename, processed_img)
        
        # Show by matplotlib
        # rows, cols = 1, 2
        # plt.subplot(rows, cols, 1)
        # plt.imread("bird.jpg")
        # plt.title("Figure 1")
        # plt.subplot(rows, cols, 2)
        # plt.show()


if __name__ == "__main__":
    process = Process()