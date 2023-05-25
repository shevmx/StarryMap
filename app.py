import pygame
import sys
from pygame.locals import *

# INITIALIZING THE GAME --------->
mainClock = pygame.time.Clock()
pygame.init()

# WINDOW SETTINGS->
WINDOW_SIZE = (int(pygame.display.Info().current_w // 2), int(pygame.display.Info().current_h // 1.6))
MONITOR_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
window_size_initial = [WINDOW_SIZE[0], WINDOW_SIZE[1]]
pygame.display.set_caption("Starry Map")
screen = pygame.display.set_mode(WINDOW_SIZE,  0, 32, pygame.RESIZABLE)
pygame.display.set_icon(pygame.image.load("data/images/icon.png"))

# LOAD THE DATA -
img_starry_map = pygame.image.load("data/images/starry_map.png")
img_map_overlay = pygame.image.load("data/images/overlay_map.png")

img_info_hover = pygame.image.load("data/images/info_hover.png")
img_info = pygame.image.load("data/images/info.png")

img_tip_map = pygame.image.load("data/images/tip_map.png")
img_tip_map_hover = pygame.image.load("data/images/tip_map_hover.png")
img_tip_map_selected = pygame.image.load("data/images/tip_map_selected.png")

img_tip_overlay = pygame.image.load("data/images/tip_overlay.png")
img_tip_overlay_selected = pygame.image.load("data/images/tip_overlay_selected.png")
img_tip_overlay_hover = pygame.image.load("data/images/tip_overlay_hover.png")

img_b_shift = pygame.image.load("data/images/startup.png")
img_b_shift_active = pygame.image.load("data/images/startup_active.png")
img_b_shift_hover = pygame.image.load("data/images/startup_hover.png")

img_fullscreen = pygame.image.load("data/images/fullscreen.png")
img_fullscreen_exit = pygame.image.load("data/images/fullscreen_exit.png")
img_fullscreen_hover = pygame.image.load("data/images/fullscreen_hover.png")
img_fullscreen_exit_hover = pygame.image.load("data/images/fullscreen_exit_hover.png")

img_guide_page1 = pygame.image.load("data/images/guide_page1.png")
img_guide_page2 = pygame.image.load("data/images/guide_page2.png")

img_arrow = pygame.image.load("data/images/back.png")
img_arrow_hover = pygame.image.load("data/images/back_hover.png")

img_close = pygame.image.load("data/images/close.png")
img_close_hover = pygame.image.load("data/images/close_hover.png")

img_scale_2x = pygame.image.load("data/images/scale_2x.png")
img_scale_2x_active = pygame.image.load("data/images/scale_2x_active.png")
img_scale_2x_hover = pygame.image.load("data/images/scale_2x_hover.png")

img_scale_x2 = pygame.image.load("data/images/scale_2x.png")
img_scale_x2_active = pygame.image.load("data/images/scale_2x_active.png")
img_scale_x2_hover = pygame.image.load("data/images/scale_2x_hover.png")

img_eye = pygame.image.load("data/images/eye.png")
img_eye_hover = pygame.image.load("data/images/eye_hover.png")
img_eye_hidden = pygame.image.load("data/images/eye_hidden.png")
img_eye_hidden_hover = pygame.image.load("data/images/eye_hidden_hover.png")

# MAIN VARIABLES ->
angleMap = 0
angleOverlay = 0
active = 0 # 0 - map; 1 - overlay
fullscreen = False

# BUTTONS STATUS ->
b_left = False
b_right = False
b_shift = False
b_scale_x2 = False
b_eye_hidden = False


def center_image(img, w_x, w_y, angle):
	global b_scale_x2

	if b_scale_x2:
		image = pygame.transform.scale(img, (w_y * 2, w_y * 2))
	else:
		image = pygame.transform.scale(img, (w_y, w_y))

	img_rect = image.get_rect()
	rot_image = pygame.transform.rotate(image, int(angle))
	rot_rect = img_rect.copy()
	rot_rect.center = rot_image.get_rect().center
	rot_image = rot_image.subsurface(rot_rect).copy()

	if b_scale_x2:
		screen.blit(rot_image, (w_x // 2 - img_rect.w // 2, -img_rect.h // 2))
	else:
		screen.blit(rot_image, (w_x // 2 - img_rect.w // 2, w_y // 2 - img_rect.h // 2))


def rotate_map(status, active, speed_angle_rotate=1.25):
	global angleMap, angleOverlay, b_shift

	if b_shift:
		speed_angle_rotate = int(speed_angle_rotate * 5)

	if status == "left":
		if active == 0:
			angleMap -= speed_angle_rotate
		elif active == 1:
			angleOverlay -= speed_angle_rotate
	elif status == "right":
		if active == 0:
			angleMap += speed_angle_rotate
		elif active == 1:
			angleOverlay += speed_angle_rotate


def window_event_handler(event):
	global MONITOR_SIZE, window_size_initial, fullscreen
	
	if event.type == QUIT:
		pygame.quit()
		sys.exit()
	if event.type == VIDEORESIZE and not fullscreen:
		if event.h < 720:
			event.h = 720
		
		if event.w / event.h != 1.5 and event.w != MONITOR_SIZE[0]:
			if window_size_initial[1] != event.h:
				event.w = int(event.h * 1.5)
			if window_size_initial[0] != event.w:
				event.h = int(event.w // 1.5)

		window_size_initial = [event.w, event.h]
		screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

	# KEY EVENTS ->	
	if event.type == KEYDOWN:
		if event.key == K_F12 and not fullscreen:
			fullscreen = True
			screen = pygame.display.set_mode(MONITOR_SIZE, pygame.FULLSCREEN, 32)
		if event.key == K_ESCAPE and fullscreen:
			fullscreen = False
			screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE, 32)


def info():
	running = True
	guide_page = 1

	while running:
		screen.fill((0, 0, 0))
		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = False
		w_x, w_y = screen.get_size()

		# CHECK EVENT ------------------->
		for event in pygame.event.get():
			window_event_handler(event=event)

			# MOUSE DOWN EVENTS ->
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
		
		# CLOSE THE GUIDE PAGE ------------->
		img_close0 = pygame.transform.scale(img_close, (w_x // 30, w_x // 30))
		img_close_rect0 = img_close0.get_rect()
		img_close_rect0.x = w_x - img_close_rect0.w - 10
		img_close_rect0.y = 10

		if img_close_rect0.collidepoint((mouse_x, mouse_y)):
			img_close_hover0 = pygame.transform.scale(img_close_hover, (w_x // 30, w_x // 30))
			screen.blit(img_close_hover0, (img_close_rect0.x, img_close_rect0.y))
		else:
			screen.blit(img_close0, (img_close_rect0.x, img_close_rect0.y))

		# BTN ARROWs ----------->
		btn_arrow = pygame.transform.scale(img_arrow, (w_x // 20, w_x // 20))
		btn_arrow_hover = pygame.transform.scale(img_arrow_hover, (w_x // 20, w_x // 20))
		btn_arrow_next = pygame.transform.flip(btn_arrow, True, False)
		btn_arrow_rect = btn_arrow.get_rect()
		btn_arrow_rect.y = w_y - btn_arrow_rect.h - 10

		# SHOW GUIDE -------------->
		i_guide_page_rect = img_guide_page1.get_rect()
		ratio = i_guide_page_rect.w / i_guide_page_rect.h

		if guide_page == 1:
			i_guide_page1 = pygame.transform.scale(img_guide_page1, (int(w_x * 0.6), int(w_x * 0.6 // ratio)))
			i_guide_page1_rect = i_guide_page1.get_rect()
			screen.blit(i_guide_page1, (int(w_x // 2 - i_guide_page1_rect.w // 2), 0))

			# BUTTON NEXT --------------->
			btn_arrow_rect.x = w_x - btn_arrow_rect.w - 10
			if btn_arrow_rect.collidepoint((mouse_x, mouse_y)):
				btn_arrow_hover_next = pygame.transform.flip(btn_arrow_hover, True, False)
				screen.blit(btn_arrow_hover_next, (btn_arrow_rect.x, btn_arrow_rect.y))
			else:
				screen.blit(btn_arrow_next, (btn_arrow_rect.x, btn_arrow_rect.y))
		elif guide_page == 2:
			i_guide_page2 = pygame.transform.scale(img_guide_page2, (int(w_x * 0.6), int(w_x * 0.6 // ratio)))
			i_guide_page2_rect = i_guide_page2.get_rect()
			screen.blit(i_guide_page2, (int(w_x // 2 - i_guide_page2_rect.w // 2), 0))

			# BACK BUTTON --------------->
			btn_arrow_rect.x = 10
			if btn_arrow_rect.collidepoint((mouse_x, mouse_y)):
				screen.blit(btn_arrow_hover, (btn_arrow_rect.x, btn_arrow_rect.y))
			else:
				screen.blit(btn_arrow, (btn_arrow_rect.x, btn_arrow_rect.y))

		# HANDLE CLICK EVENTS ------------->
		if click:
			if img_close_rect0.collidepoint((mouse_x, mouse_y)):
				running = False
			elif btn_arrow_rect.collidepoint((mouse_x, mouse_y)):
				if guide_page == 1:
					guide_page = 2
				elif guide_page == 2:
					guide_page = 1

		# UPDATE SCREEN ------------------->
		pygame.display.update()
		mainClock.tick(30)


info()

# START FROGRAM ------------>
running = True
while running:
	screen.fill((0, 0, 0))
	mouse_x, mouse_y = pygame.mouse.get_pos()
	click = False
	w_x, w_y = screen.get_size()

	# CHECK EVENT ------------------->
	for event in pygame.event.get():
		window_event_handler(event)

		# KEY EVENTS ->
		if event.type == KEYDOWN:
			if event.key == K_LEFT:
				b_left = True
			if event.key == K_RIGHT:
				b_right = True
			if pygame.key.get_mods() & pygame.KMOD_SHIFT:
				if b_shift:
					b_shift = False
				else:
					b_shift = True

		if event.type == KEYUP:
			if event.key == K_LEFT:
				b_left = False
			if event.key == K_RIGHT:
				b_right = False

		# MOUSE DOWN EVENTS ->
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				click = True

			if event.button == 4:
				rotate_map(status="left", active=active)

			if event.button == 5:
				rotate_map(status="right", active=active)

	# MOVE IMAGE ------------->
	if b_right:
		rotate_map(status="right", active=active)
	if b_left:
		rotate_map(status="left", active=active)

	# TIP MAP ->
	icons_ratio_sum = int(w_x // 2 + (w_x // 2) // 2)
	icons_ratio_sub = int(w_y // 2 - (w_y // 2) // 1.5)
	img_tip_map_rect = img_tip_map.get_rect()
	i_ratio = img_tip_map_rect.w / img_tip_map_rect.h
	tips_ratio = w_y // 6

	i_map = pygame.transform.scale(img_tip_map, (tips_ratio, int(tips_ratio // i_ratio)))
	i_map_rect = i_map.get_rect()
	i_map_rect.x = w_x - i_map_rect.w - 10
	i_map_rect.y = w_y - i_map_rect.h - 10

	if active == 0:
		i_map_active = pygame.transform.scale(img_tip_map_selected, (tips_ratio, int(tips_ratio // i_ratio)))
		screen.blit(i_map_active, (i_map_rect.x, i_map_rect.y))
	else:
		if i_map_rect.collidepoint((mouse_x, mouse_y)):
			i_map_hover = pygame.transform.scale(img_tip_map_hover, (tips_ratio, int(tips_ratio // i_ratio)))
			screen.blit(i_map_hover, (i_map_rect.x, i_map_rect.y))
		else:
			screen.blit(i_map, (i_map_rect.x, i_map_rect.y))

	center_image(img_starry_map, w_x, w_y, angleMap)

	# TIP OVERLAY ->
	img_tip_overlay_rect = img_tip_overlay.get_rect()
	i_ratio = img_tip_overlay_rect.w / img_tip_overlay_rect.h
	i_overlay = pygame.transform.scale(img_tip_overlay, (tips_ratio, int(tips_ratio // i_ratio)))
	i_overlay_rect = i_overlay.get_rect()

	if not b_eye_hidden:
		i_overlay_rect.x = w_x - i_overlay_rect.w - 10
		i_overlay_rect.y = w_y - i_overlay_rect.h * 2 - 20

		if active == 1:
			i_overlay_active = pygame.transform.scale(img_tip_overlay_selected, (tips_ratio, int(tips_ratio // i_ratio)))
			screen.blit(i_overlay_active, (i_overlay_rect.x, i_overlay_rect.y))
		else:
			if i_overlay_rect.collidepoint((mouse_x, mouse_y)):
				i_overlay_hover = pygame.transform.scale(img_tip_overlay_hover, (tips_ratio, int(tips_ratio // i_ratio)))
				screen.blit(i_overlay_hover, (i_overlay_rect.x, i_overlay_rect.y))
			else:
				screen.blit(i_overlay, (i_overlay_rect.x, i_overlay_rect.y))

		center_image(img_map_overlay, w_x, w_y, angleOverlay)
	else:
		i_overlay_rect.y = -200
		active = 0

	# BUTTONS ------------------------->
	icon_btn_ratio = w_y // 25

	# BTN FULLSCREEN ->
	i_fullscreen = pygame.transform.scale(img_fullscreen, (icon_btn_ratio, icon_btn_ratio))
	i_fullscreen_rect = i_fullscreen.get_rect()
	i_fullscreen_rect.x = 10
	i_fullscreen_rect.y = w_y - 10 - i_fullscreen_rect.w

	if fullscreen:
		if i_fullscreen_rect.collidepoint((mouse_x, mouse_y)):
			i_fullscreen_exit_hover = pygame.transform.scale(img_fullscreen_exit_hover, (icon_btn_ratio, icon_btn_ratio))
			screen.blit(i_fullscreen_exit_hover, (i_fullscreen_rect.x, i_fullscreen_rect.y))
		else:
			i_fullscreen_exit = pygame.transform.scale(img_fullscreen_exit, (icon_btn_ratio, icon_btn_ratio))
			screen.blit(i_fullscreen_exit, (i_fullscreen_rect.x, i_fullscreen_rect.y))
	elif not fullscreen:
		if i_fullscreen_rect.collidepoint((mouse_x, mouse_y)):
			i_fullscreen_hover = pygame.transform.scale(img_fullscreen_hover, (icon_btn_ratio, icon_btn_ratio))
			screen.blit(i_fullscreen_hover, (i_fullscreen_rect.x, i_fullscreen_rect.y))
		else:
			screen.blit(i_fullscreen, (i_fullscreen_rect.x, i_fullscreen_rect.y))

	d_ratio = int(i_fullscreen_rect.w // 2) + 12

	# BTN INFO ->
	i_info = pygame.transform.scale(img_info, (icon_btn_ratio, icon_btn_ratio))
	i_info_rect = i_info.get_rect()
	i_info_rect.x = d_ratio * 2
	i_info_rect.y = w_y - 10 - i_fullscreen_rect.w

	if i_info_rect.collidepoint((mouse_x, mouse_y)):
		i_info_hover = pygame.transform.scale(img_info_hover, (icon_btn_ratio, icon_btn_ratio))
		screen.blit(i_info_hover, (i_info_rect.x, i_info_rect.y))
	else:
		screen.blit(i_info, (i_info_rect.x, i_info_rect.y))

	# BTN STARTUP ->
	i_speedup = pygame.transform.scale(img_b_shift, (icon_btn_ratio, icon_btn_ratio))
	i_speedup_rect = i_speedup.get_rect()
	i_speedup_rect.x = d_ratio * 3 + 15
	i_speedup_rect.y = w_y - 10 - i_fullscreen_rect.w

	if b_shift:
		i_speedup_active = pygame.transform.scale(img_b_shift_active, (icon_btn_ratio, icon_btn_ratio))
		screen.blit(i_speedup_active, (i_speedup_rect.x, i_speedup_rect.y))
	else:
		if i_speedup_rect.collidepoint((mouse_x, mouse_y)):
			i_speedup_hover = pygame.transform.scale(img_b_shift_hover, (icon_btn_ratio, icon_btn_ratio))
			screen.blit(i_speedup_hover, (i_speedup_rect.x, i_speedup_rect.y))
		else:
			screen.blit(i_speedup, (i_speedup_rect.x, i_speedup_rect.y))

	# BTN SCALE X2 ->
	i_scale_x2 = pygame.transform.scale(img_scale_x2, (icon_btn_ratio, icon_btn_ratio))
	i_scale_x2_rect = i_scale_x2.get_rect()
	i_scale_x2_rect.x = d_ratio * 4 + 30
	i_scale_x2_rect.y = w_y - 10 - i_fullscreen_rect.w

	if b_scale_x2:
		i_scale_x2_active = pygame.transform.scale(img_scale_x2_active, (icon_btn_ratio, icon_btn_ratio))
		screen.blit(i_scale_x2_active, (i_scale_x2_rect.x, i_scale_x2_rect.y))
	else:
		if i_scale_x2_rect.collidepoint((mouse_x, mouse_y)):
			i_scale_x2_hover = pygame.transform.scale(img_scale_x2_hover, (icon_btn_ratio, icon_btn_ratio))
			screen.blit(i_scale_x2_hover, (i_scale_x2_rect.x, i_scale_x2_rect.y))
		else:
			screen.blit(i_scale_x2, (i_scale_x2_rect.x, i_scale_x2_rect.y))

	# BTN EYE ->
	i_eye = pygame.transform.scale(img_eye, (icon_btn_ratio, icon_btn_ratio))
	i_eye_rect = i_eye.get_rect()
	i_eye_rect.x = d_ratio * 5 + 45
	i_eye_rect.y = w_y - 10 - i_fullscreen_rect.w

	if b_eye_hidden:
		if i_eye_rect.collidepoint((mouse_x, mouse_y)):
			i_eye_hidden_hover = pygame.transform.scale(img_eye_hidden_hover, (icon_btn_ratio, icon_btn_ratio))
			screen.blit(i_eye_hidden_hover, (i_eye_rect.x, i_eye_rect.y))
		else:
			i_eye_hidden = pygame.transform.scale(img_eye_hidden, (icon_btn_ratio, icon_btn_ratio))
			screen.blit(i_eye_hidden, (i_eye_rect.x, i_eye_rect.y))
	else:
		if i_eye_rect.collidepoint((mouse_x, mouse_y)):
			i_eye_hover = pygame.transform.scale(img_eye_hover, (icon_btn_ratio, icon_btn_ratio))
			screen.blit(i_eye_hover, (i_eye_rect.x, i_eye_rect.y))
		else:
			screen.blit(i_eye, (i_eye_rect.x, i_eye_rect.y))
		
	# CLICK EVENT ----------------->
	if click:
		if i_map_rect.collidepoint((mouse_x, mouse_y)):
			active = 0
		elif i_overlay_rect.collidepoint((mouse_x, mouse_y)):
			active = 1
		elif i_fullscreen_rect.collidepoint((mouse_x, mouse_y)):
			if fullscreen:
				fullscreen = False
				screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE, 32)
			else:
				fullscreen = True
				screen = pygame.display.set_mode(MONITOR_SIZE, pygame.FULLSCREEN, 32)	
		elif i_info_rect.collidepoint((mouse_x, mouse_y)):
			info()
		elif i_speedup_rect.collidepoint((mouse_x, mouse_y)):
			if b_shift:
				b_shift = False
			else:
				b_shift = True
		elif i_scale_x2_rect.collidepoint((mouse_x, mouse_y)):
			if b_scale_x2:
				b_scale_x2 = False
			else:
				b_scale_x2 = True
		elif i_eye_rect.collidepoint((mouse_x, mouse_y)):
			if b_eye_hidden:
				b_eye_hidden = False
			else:
				b_eye_hidden = True


	# UPDATE SCREEN ------------------->
	pygame.display.update()
	mainClock.tick(30)

