# ExRelease Export v0.4
# Author: Southrop
# This macro is designed to be used with AVS scripts generated by ExRelease for quick and easy exporting of bookmarked frames.

import os.path
import pyavs

self = avsp.GetWindow()

tabcount = avsp.GetTabCount()
count = 0
currtab = avsp.GetCurrentTabIndex()

total_frames = tabcount*len(avsp.GetBookmarkList())
progress = avsp.ProgressBox(total_frames, '', 'Saving images...')

for n in range(0,tabcount):
	avsp.SelectTab(index=n)
	avsp.ShowVideoFrame(framenum=0, index=n, forceRefresh=True)

	# Sets output directory to the current working directory (where the main video file is stored)
	vidpath = avsp.GetVar('vidfile', index=n)
	dirname = os.path.dirname(vidpath)
	
	# Sets filenames to #####_Group.png format, where ##### is the frame number
	basename = ur'%06d_' + avsp.GetVar('group', index=n) + '.png'
	
	filename = os.path.join(dirname, basename)
	
	# Get list of frames
	frame_count = avsp.GetVideoFramecount(index=n)
	bookmarks = avsp.GetBookmarkList()
	if bookmarks:
		frames = sorted(filter(lambda x: x < frame_count, set(bookmarks))),
	else:
		avsp.MsgBox('There are no bookmarks set.', 'Error')
		avsp.SafeCall(progress.Destroy)
		return
	
	# Save the images
	paths = []
	AVS = pyavs.AvsClip(avsp.GetText(index=n, clean=True), matrix=self.matrix, interlaced=self.interlaced, swapuv=self.swapuv)
	if AVS.IsErrorClip():
		avsp.MsgBox(AVS.error_message, 'Error')
		return
	
	for i, frame_range in enumerate(frames):
		frame_index = len(paths) + 1
		for j, frame in enumerate(frame_range):
			if not avsp.SafeCall(progress.Update, count+len(paths), str(count+len(paths)) + ' / ' + str(total_frames))[0]:
				break
			ret = self.SaveImage(filename % (frame), frame=frame, index=n, quality=100, depth=8, avs_clip=AVS)
			if not ret:
				break
			paths.append(ret)
	
	count += len(paths)

# Clean up
avsp.SafeCall(progress.Destroy)
avsp.SelectTab(currtab)
avsp.HideVideoWindow()
avsp.MsgBox(str(count)+' images ('+str(count/tabcount)+' for each of '+str(tabcount)+' releases) created.', 'Information')
return 0