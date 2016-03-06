import os, glob, csv
import pandas as pd
import pydicom


image_dir = ['AcquisitionMatrix',
'AcquisitionNumber',
'AcquisitionTime',
'AngioFlag',
'BitsAllocated',
'BitsStored',
'BodyPartExamined',
'CardiacNumberOfImages',
'Columns',
'CommentsOnThePerformedProcedureStep',
'EchoNumbers',
'EchoTime',
'EchoTrainLength',
'FlipAngle',
'HighBit',
'ImageOrientationPatient',
'ImagePositionPatient',
'ImageType',
'ImagedNucleus',
'ImagingFrequency',
'InPlanePhaseEncodingDirection',
'InstanceCreationTime',
'InstanceNumber',
'LargestImagePixelValue',
'MRAcquisitionType',
'MagneticFieldStrength',
'Manufacturer',
'ManufacturerModelName',
'Modality',
'NominalInterval',
'NumberOfAverages',
'NumberOfPhaseEncodingSteps',
'PatientAddress',
'PatientAge',
'PatientBirthDate',
'PatientID',
'PatientName',
'PatientPosition',
'PatientSex',
'PatientTelephoneNumbers',
'PercentPhaseFieldOfView',
'PercentSampling',
'PerformedProcedureStepID',
'PerformedProcedureStepStartTime',
'PhotometricInterpretation',
'PixelBandwidth',
'PixelRepresentation',
'PixelSpacing',
'PositionReferenceIndicator',
'RefdImageSequence',
'ReferencedImageSequence',
'RepetitionTime',
'Rows',
'SAR',
'SOPClassUID',
'SOPInstanceUID',
'SamplesPerPixel',
'ScanOptions',
'ScanningSequence',
'SequenceName',
'SequenceVariant',
'SeriesDescription',
'SeriesNumber',
'SeriesTime',
'SliceLocation',
'SliceThickness',
'SmallestImagePixelValue',
'SoftwareVersions',
'SpecificCharacterSet',
'StudyTime',
'TransmitCoilName',
'TriggerTime',
'VariableFlipAngleFlag',
'WindowCenter',
'WindowCenterWidthExplanation',
'WindowWidth',
'dBdt']


def get_data(train_or_validate):
    data_path = 'data/{}'.format(train_or_validate)

    patient_folders = glob.glob(os.path.join(data_path, '*'))

    i = 0

    # get the age and sex of each patient, add it to the data list
    for folder in patient_folders:
        image_folders = glob.glob(os.path.join(folder, 'study', '*'))
        for img_folder in image_folders:
            images = glob.glob(os.path.join(img_folder, '*'))
            for image_file in images:
                data = pd.DataFrame(columns=image_dir+['ImagePath'])
                image = pydicom.read_file(image_file)
                for attr in image_dir:
                    if hasattr(image, attr):
                        data.loc[0, attr] = getattr(image, attr)
                data.loc[0, 'ImagePath'] = image_file
                with open('metadata_{}.csv'.format(train_or_validate), 'a') as f:
                    if i==0:
                        data.to_csv(f, header=True, index=False)
                    else:
                        data.to_csv(f, header=False, index=False)
                i += 1
                if i%100==0:
                    print i, image_file

    # sort the data list by patient number, then save to a csv file
    #df = pd.DataFrame(data[1:], columns=data[0])
    #df['patient'] = df['patient'].astype(int)
    #df = df.sort_values(by='patient')
    #df = df[['age', 'sex']]
    #df.to_csv('age_sex_{}.csv'.format(train_or_validate), index=False)
    #data.to_csv('metadata.csv', index=False)


if __name__ == '__main__':
    #get_data('train')
    get_data('validate')