# Standard library
import sys, os.path

# Additional library
import numpy

def HIStoArray(filename):
    file = open(filename, 'rb')
    header = file.read(64) # read first 64 bytes "IM" header
    while header:
        if header.startswith("IM"):
            tmp = str(hex(ord(header[3:4]))[2:]) + str(hex(ord(header[2:3]))[2:])
            commentLength = int("0x" + tmp, 0)
            tmp = str(hex(ord(header[5:6]))[2:]) + str(hex(ord(header[4:5]))[2:])
            iDX = int("0x" + tmp, 0)
            tmp = str(hex(ord(header[7:8]))[2:]) + str(hex(ord(header[6:7]))[2:])
            iDY = int("0x" + tmp, 0)
            dataLength = iDX * iDY *2
            tmp = str(hex(ord(header[9:10]))[2:]) + str(hex(ord(header[8:9]))[2:])
            iX = int("0x" + tmp, 0)
            tmp = str(hex(ord(header[11:12]))[2:]) + str(hex(ord(header[10:11]))[2:])
            iY = int("0x" + tmp, 0)
            tmp = str(hex(ord(header[13:14]))[2:]) + str(hex(ord(header[12:13]))[2:])
            filetype = int("0x" + tmp, 0)
            a = str(hex(ord(header[15:16]))[2:])
            b = str(hex(ord(header[14:15]))[2:])
            tmp = a.zfill(2) + b.zfill(2)
            numberofImages = int("0x" + tmp, 0)
        elif header.startswith("[Application]"):
            applicationHeader = header.rstrip().split(",")
        elif header.startswith("[Acquisition]"):
            acquisitionHeader = header.rstrip().split(',')
            for header in acquisitionHeader:
                if header.startswith("ExposureTime"):
                     exposureTime = header.split("=")[1].replace("ms", "").rstrip()
        elif header.startswith("[Grabber]"):
            grabberHeader = header.rstrip().split(',')
        elif header.startswith("[DisplayLUT]"):
            displayLUTHeader = header.rstrip().split(',')
        elif header.startswith("[Scaling]"):
            scalingHeader = header.rstrip().split(',')
        elif header.startswith("[Camera]"):
            cameraHeader = header.rstrip().split(',')
            break
        header = file.readline()

    test = file.read(2)
    stack = []
    # Load each image
    for i in range(0, numberofImages):
        test = file.read(dataLength)
        #spectrumized = numpy.fromstring(test, dtype=numpy.uint16).reshape((iDY, iDX)).sum(axis=0) / (float(exposureTime) / 1000.) # Onedimentionalize
        #spectrumized_tmp = numpy.fromstring(test, dtype=numpy.uint16).reshape((iDY, iDX))
        #if i < 100:
            #numpy.savetxt(filename + str(i) +"_raw2d.dat", spectrumized_tmp, fmt="%s")
        #spectrumized = numpy.fromstring(test, dtype=numpy.uint16).reshape((iDY, iDX)).sum(axis=0) / (float(exposureTime) / 1000.) # Onedimentionalize
        spectrumized = numpy.fromstring(test, dtype=numpy.uint16).reshape((iDY, iDX)).sum(axis=0) # Onedimentionalize
        exposureTimems = float(exposureTime) / 1000.
        #if i < 100:
            #numpy.savetxt(filename + str(i) +"_raw1d.dat", spectrumized, fmt="%s")
        stack.append(spectrumized)
        test = file.read(64) # remove IM header
    #numpy.savetxt(filename + "_raw.dat", stack, fmt="%s", delimiter=' ')
    #numpy.savetxt(filename + "_raw2d.dat", spectrumized_tmp, fmt="%s")
    return stack, exposureTimems

def ex3toenergy(filename):
    energy = []
    file = open(filename, 'r')
    line = file.readline()
    while line:
        if line.startswith("[EX_BEGIN]"):
            while line:
                line = file.readline()
                if line == "" or line == "\n":
                    break
                elif line.startswith("[EX_END]"):
                    break
                else:
                    e = line.split("\t")[0]
                    energy.append(e)
        line = file.readline()
    file.close
    return energy

def convertHIStospectrum(datafile, darkfordatafile, blankfile, darkforblankfile, calibrationfile,
                         start_frame_number, number_of_spectra, accumulation_frames,
                         accumulation_axis, activate_dark, repeat_black_and_dark
                         ):
    dataStack, dataStackExposureTime = HIStoArray(datafile)
    darkforDataStack, darkforDataStackExposureTime = HIStoArray(darkfordatafile)
    blankDataStack, blankDataStackExposureTime = HIStoArray(blankfile)
    darkforBlankDataStack, darkforBlankDataStackExposureTime = HIStoArray(darkforblankfile)
    energy = numpy.array(ex3toenergy(calibrationfile))

    i = 0
    stack = []
    if number_of_spectra == 0:
        number_of_images = len(dataStack) + 1
    else:
        number_of_images = min(start_frame_number + accumulation_frames * number_of_spectra, len(dataStack) + 1)

    #for i in range((start_frame_number - 1), (start_frame_number + accumulation_frames * number_of_spectra - 1)):
    for i in range((start_frame_number - 1), (number_of_images - 1)):
        data = dataStack[i]
        id = i % accumulation_frames
        darkfordata = darkforDataStack[id]
        blankdata = blankDataStack[id]
        darkforblank = darkforBlankDataStack[id]

        if id == 0:
            dataall = data
            darkfordataall = darkfordata
            blankall = blankdata
            darkforblankall = darkforblank
        else:
            dataall = dataall + data
            darkfordataall = darkfordataall + darkfordata
            blankall = blankall + blankdata
            darkforblankall = darkforblankall + darkforblank

        if ((i + 1) % accumulation_frames) == 0:
            spectrum = - numpy.log(numpy.divide(((dataall - darkfordataall).astype(numpy.float) / dataStackExposureTime), ((blankall - darkforblankall).astype(numpy.float) / blankDataStackExposureTime)))
            stack.append(spectrum[::-1])
            del(dataall)
            del(darkfordataall)
            del(blankall)
            del(darkforblankall)
            del(spectrum)

    savefilename, ext = os.path.splitext(datafile)

    for i in range (0, len(stack)):
        test = numpy.transpose(numpy.concatenate([[energy],[stack.pop(0)]]))
        numpy.savetxt(savefilename + "_" + str(i+1).zfill(3) + ".dat", test, fmt="%s", delimiter='\t')
