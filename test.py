import cv2
import numpy as np

# Function to calculate the ratio of "on" pixels in a mask
def calculate_on_pixel_ratio(mask):
	total_pixels = mask.size
	on_pixels = cv2.countNonZero(mask)
	return on_pixels / total_pixels


# Blue health bars
lower_blue = np.array([20, 80, 160]) 
upper_blue = np.array([100, 170, 255])

# Red health bars

lower_red = np.array([120, 10, 35])
upper_red = np.array([255, 90, 100])

# Load the enemy image
image_ennemy = cv2.imread('D:\\clash royale\\Bot-Clash-Royal-2024\\image_ennemy_2.png')


# Convert the enemy image to HSV color space
rgb_ennemy = cv2.cvtColor(image_ennemy, cv2.COLOR_BGR2RGB)
#cv2.imshow('image', rgb_ennemy)


# Create masks for blue and red health bars in the enemy image
mask_blue_ennemy = cv2.inRange(rgb_ennemy, lower_blue, upper_blue)
mask_red_ennemy = cv2.inRange(rgb_ennemy, lower_red, upper_red)

# Resize the masks to make them appear bigger
scale_factor_ennemy = 2.5
mask_blue_ennemy = cv2.resize(mask_blue_ennemy, None, fx=scale_factor_ennemy, fy=scale_factor_ennemy, interpolation=cv2.INTER_LINEAR)
mask_red_ennemy = cv2.resize(mask_red_ennemy, None, fx=scale_factor_ennemy, fy=scale_factor_ennemy, interpolation=cv2.INTER_LINEAR)

# Add green space between the two masks
green_space = np.full((mask_blue_ennemy.shape[0], 10), 255, dtype=np.uint8)  # 10 pixels wide green space

# Combine the masks with green space
mask_combined_ennemy = cv2.hconcat([mask_blue_ennemy, green_space, mask_red_ennemy])

# Convert the combined mask to BGR color space and add green color
mask_combined_ennemy_bgr = cv2.cvtColor(mask_combined_ennemy, cv2.COLOR_GRAY2BGR)
mask_combined_ennemy_bgr[:, mask_blue_ennemy.shape[1]:mask_blue_ennemy.shape[1] + 10] = [0, 255, 0]  # Green color

# Load the ally image

image_ally = cv2.imread('D:\\clash royale\\Bot-Clash-Royal-2024\\image_ally_2.png')

# Convert the ally image to HSV color space
rgb_ally = cv2.cvtColor(image_ally, cv2.COLOR_BGR2RGB)

# Create masks for blue and red health bars in the ally image
mask_blue_ally = cv2.inRange(rgb_ally, lower_blue, upper_blue)
mask_red_ally = cv2.inRange(rgb_ally, lower_red, upper_red)

# Resize the masks to make them appear bigger with a different scale factor
scale_factor_ally = 2
mask_blue_ally = cv2.resize(mask_blue_ally, None, fx=scale_factor_ally, fy=scale_factor_ally, interpolation=cv2.INTER_LINEAR)
mask_red_ally = cv2.resize(mask_red_ally, None, fx=scale_factor_ally, fy=scale_factor_ally, interpolation=cv2.INTER_LINEAR)

# Add green space between the two masks
green_space_ally = np.full((mask_blue_ally.shape[0], 10), 255, dtype=np.uint8)  # 10 pixels wide green space

# Combine the masks with green space
mask_combined_ally = cv2.hconcat([mask_blue_ally, green_space_ally, mask_red_ally])

# Convert the combined mask to BGR color space and add green color
mask_combined_ally_bgr = cv2.cvtColor(mask_combined_ally, cv2.COLOR_GRAY2BGR)
mask_combined_ally_bgr[:, mask_blue_ally.shape[1]:mask_blue_ally.shape[1] + 10] = [0, 255, 0]  # Green color

# Ensure the widths of the enemy and ally masks are the same
width = max(mask_combined_ennemy_bgr.shape[1], mask_combined_ally_bgr.shape[1])
mask_combined_ennemy_bgr = cv2.copyMakeBorder(mask_combined_ennemy_bgr, 0, 0, 0, width - mask_combined_ennemy_bgr.shape[1], cv2.BORDER_CONSTANT, value=[0, 0, 0])
mask_combined_ally_bgr = cv2.copyMakeBorder(mask_combined_ally_bgr, 0, 0, 0, width - mask_combined_ally_bgr.shape[1], cv2.BORDER_CONSTANT, value=[0, 0, 0])

# Add green space between the enemy and ally masks
green_space_between = np.full((10, width, 3), [0, 255, 0], dtype=np.uint8)  # 10 pixels wide green space

# Combine the enemy and ally masks vertically
final_combined = cv2.vconcat([mask_combined_ennemy_bgr, green_space_between, mask_combined_ally_bgr])

# Calculate the ratio of "on" pixels for each mask
ratio_blue_ennemy = calculate_on_pixel_ratio(mask_blue_ennemy)
ratio_red_ennemy = calculate_on_pixel_ratio(mask_red_ennemy)
ratio_blue_ally = calculate_on_pixel_ratio(mask_blue_ally)
ratio_red_ally = calculate_on_pixel_ratio(mask_red_ally)

# Print the ratios
print(f"Enemy - Blue vs Red ratio: {ratio_blue_ennemy:.2f} vs {ratio_red_ennemy:.2f}")
print(f"Ally - Blue vs Red ratio: {ratio_blue_ally:.2f} vs {ratio_red_ally:.2f}")


# Show the final combined mask result
cv2.imshow('Mask', final_combined)

cv2.waitKey(0)
cv2.destroyAllWindows()



