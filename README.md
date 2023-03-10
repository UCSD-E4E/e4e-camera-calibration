# E4E Camera Calibration tool
This repo contains a camera calibration tool and procedure.

## Perform Stereo Camera Calibration
```bash
python e4e_camera_calibration calibrate --display-error --camera qoocam-ego --calibration-directory ./data/qoocam/calibration --output ./calibration-output.dat
```

## Perform Disparity Parameter Search
This leverages Sherlock to perform a parameter search to choose the best parameter for generating the disparity map.  It does this by generating a disparity map for each of parameter sets that Sherlock chooses.  It then calculates the size of checkerboard squares and compares those with the known ground truth.  It calculates the RMSE error and attempts to optimize that error.

```bash
python ./e4e_camera_calibration tune-disparity  --display-error --camera qoocam-ego --calibration-directory ./data/qoocam/calibration --calibration-tables ./calibration-output.dat
```