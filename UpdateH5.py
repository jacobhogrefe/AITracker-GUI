import numpy as np
import h5py
from matplotlib import pyplot as plt

# # Updates labels in H5 files as they are saved in old data collection app
# def update_labels(input_h5_path, output_h5_path, substring_to_label_mapping):
#     # Open the input H5 file in read mode
#     with h5py.File(input_h5_path, 'r') as h5_file:
#         # Check if the 'labels' dataset exists
#         if 'labels' not in h5_file:
#             print("Error: 'labels' dataset not found in the H5 file.")
#             return
#
#         # Read the existing labels
#         existing_labels = h5_file['labels'][:]
#
#         # Update the labels based on the specified substrings
#         updated_labels = []
#
#         for old_label in existing_labels:
#             updated_label = old_label
#
#             for substring, new_label in substring_to_label_mapping.items():
#                 if substring.encode('utf-8') in old_label:
#                     updated_label = new_label.encode('utf-8')
#                     break
#
#             updated_labels.append(updated_label)
#
#         # Convert string labels to bytes using a loop
#         updated_labels_bytes = np.array([label for label in updated_labels], dtype='S')
#
#         # Create a new H5 file for the updated data
#         with h5py.File(output_h5_path, 'w') as output_h5_file:
#             # Copy other datasets from the input file to the output file
#             for dataset_name in h5_file.keys():
#                 if dataset_name != 'labels':
#                     h5_file.copy(dataset_name, output_h5_file)
#
#             # Create a new 'labels' dataset with the updated labels as bytes
#             output_h5_file.create_dataset('labels', data=updated_labels_bytes)
#
#     print(f"Updated H5 file saved to '{output_h5_path}'.")
#
# # Example usage:
# substring_to_label_mapping = {
#     'northwest': 'North West',
#     'northeast': 'North East',
#     'southwest': 'South West',
#     'southeast': 'South East',
#     'north': 'North',
#     'south': 'South',
#     'west': 'West',
#     'east': 'East',
#     'center': 'Center'
# }
#
#
# # Specify the path to your input H5 file and the desired output path
# input_h5_path = 'H5Demo/eye_data.h5'
# output_h5_path = 'H5Demo/final_eye_data.h5'
#
# # Update labels using the custom_label_update function and save to a new path
# update_labels(input_h5_path, output_h5_path, substring_to_label_mapping)

# # Read and display first few images and labels in an H5 file
# def readH5(path):
#     # Open the HDF5 file for reading
#     h5f = h5py.File(path, 'r')
#
#     # Read the 'images' and 'labels' datasets
#     images = h5f['images'][:]
#     labels = h5f['labels'][:]
#
#     # Close the HDF5 file
#     h5f.close()
#
#     # Display the images
#     for i in range(len(images)):
#         label = labels[i].decode()  # Decode the label from bytes to string
#         plt.figure()
#         plt.imshow(images[i])
#         plt.title(f"Label: {label}")
#         plt.show()
#
# readH5('H5Demo/final_eye_data.h5')

# # Prints all labels in an H5 File
# def print_labels(h5_file_path):
#     # Open the H5 file in read mode
#     with h5py.File(h5_file_path, 'r') as h5_file:
#         # Check if the 'labels' dataset exists
#         if 'labels' not in h5_file:
#             print("Error: 'labels' dataset not found in the H5 file.")
#             return
#
#         # Read the labels
#         labels = h5_file['labels'][:]
#
#         # Print each label
#         for label in labels:
#             print(label.decode('utf-8'))
#
# # Example usage:
# h5_file_path = 'H5Demo/final_eye_data.h5'
# print_labels(h5_file_path)



## Combines two H5 files into a single H5 file
# def combine_h5_files(input_h5_file1, input_h5_file2, output_h5_file):
#     # Open the first input H5 file in read mode
#     with h5py.File(input_h5_file1, 'r') as h5_file1:
#         # Read data from the first file
#         images1 = h5_file1['images'][:]
#         labels1 = h5_file1['labels'][:]
#
#     # Open the second input H5 file in read mode
#     with h5py.File(input_h5_file2, 'r') as h5_file2:
#         # Read data from the second file
#         images2 = h5_file2['images'][:]
#         labels2 = h5_file2['labels'][:]
#
#     # Combine the data from the two files
#     combined_images = np.concatenate((images1, images2), axis=0)
#     combined_labels = np.concatenate((labels1, labels2), axis=0)
#
#     # Create a new H5 file for the combined data
#     with h5py.File(output_h5_file, 'w') as output_h5_file:
#         # Create datasets in the new file
#         output_h5_file.create_dataset('images', data=combined_images)
#         output_h5_file.create_dataset('labels', data=combined_labels)
#
#     print(f"Data from '{input_h5_file1}' and '{input_h5_file2}' combined and saved to '{output_h5_file}'.")
#
#
# input_h5_file1_path = 'H5Demo/output_train.h5'
# input_h5_file2_path = 'H5Demo/output_test.h5'
# output_h5_file_path = 'H5Demo/eye_data.h5'
#
# combine_h5_files(input_h5_file1_path, input_h5_file2_path, output_h5_file_path)


import h5py
from PIL import Image
import numpy as np

def clean_label(label):
    # Remove any quotation marks from the label and decode it if it's in bytes
    cleaned_label = label.decode('utf-8').replace('"', '').replace("'", "") if isinstance(label, bytes) else label
    return cleaned_label

def h5_to_jpg_batch_with_labels(h5_file_path, output_folder):
    try:
        # Convert output_folder to string if it's a bytes-like object
        output_folder = output_folder.decode('utf-8') if isinstance(output_folder, bytes) else output_folder

        # Open the H5 file
        with h5py.File(h5_file_path, 'r') as h5_file:
            # Assuming the images are stored in a dataset named 'images' and labels in a dataset named 'labels'
            images_dataset = h5_file['images']
            labels_dataset = h5_file['labels']

            # Get the first 5 images and labels (assuming the dataset is 3D with dimensions: (num_images, height, width))
            for i in range(10):
                image_data = images_dataset[i]
                label = labels_dataset[i]

                # Clean the label by removing quotation marks and decoding it if it's in bytes
                cleaned_label = clean_label(label)

                # Convert the image data to a PIL Image
                pil_image = Image.fromarray(np.uint8(image_data))

                # Save the image as a JPEG file with the cleaned label as the filename and numbering
                output_path = f"{output_folder}/{cleaned_label}_image_{i + 1}.jpg"
                pil_image.save(output_path, format='JPEG')

                print(f"Successfully saved image {i + 1} with label '{cleaned_label}' as {output_path}")

    except Exception as e:
        print(f"Error: {e}")


h5_file_path = 'H5Demo/final_eye_data.h5'
output_folder = 'NetworkDemo'
h5_to_jpg_batch_with_labels(h5_file_path, output_folder)