import argparse
import matplotlib.pyplot as plt

def main():    
    parser = argparse.ArgumentParser(description="Create a plots from a rover log.  Each plot will be \
        saved as an individual file in the local directory.")
    parser.add_argument("filepath")
    parser.add_argument('-a','--all',action='store_true',help="Create all available plots.  Default if no options are given.")
    parser.add_argument('--sonar_plot',action='store_true',help="Create a plot of sonar data.")
    parser.add_argument('--steering_plot',action='store_true',help="Create a plot of commanded steering data.")

    args = parser.parse_args()

    # if no specific output option is request then all ouput options will be completed
    if not (args.all or args.sonar_plot or args.steering_plot):
        args.all = True

    # Create a plot for sonar data
    if args.all == True or args.sonar_plot:
        sonar_1 = []
        sonar_2 = []
        sonar_3 = []
        sonar_4 = []
        sonar_5 = []
        with open(args.filepath) as fp:
            cnt5 = 0
            x_sonar=[]
            for line in fp:
                words = line.strip().split(':')
                if words[0] == '65':
                    cnt5 +=1
                    x_sonar.append(cnt5)
                    sonar_1.append(int(words[1]))                
                    sonar_2.append(int(words[2]))                
                    sonar_3.append(int(words[3]))                
                    sonar_4.append(int(words[4]))                
                    sonar_5.append(int(words[5]))                

        plt.clf()
        plt.plot(x_sonar,sonar_1, label = "far left")
        plt.plot(x_sonar,sonar_2, label = "mid left")
        plt.plot(x_sonar,sonar_3, label = "front")
        plt.plot(x_sonar,sonar_4, label = "mid right")
        plt.plot(x_sonar,sonar_5, label = "far right")
        plt.xlim(-5,cnt5+20)
        plt.legend()
        plt.savefig("sonar_plot.png")

    # Create a plot for commanded steering data
    if args.all == True or args.steering_plot:
        steering = []
        with open(args.filepath) as fp:
            cnt6 = 0
            x_steer=[]
            for line in fp:
                words = line.strip().split(':')
                if words[0] == '128':
                    cnt6 +=1
                    x_steer.append(cnt6)
                    steering.append(int(words[2]))                

        plt.clf()
        plt.plot(x_steer,steering)
        plt.savefig("steering_plot.png")
    
if __name__ == '__main__':
    main()
