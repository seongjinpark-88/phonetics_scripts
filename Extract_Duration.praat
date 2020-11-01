# Original script is from praat scripts in Internet (4.7.2003 Mietta Lennes)
# Modified by Seongjin 12.21.2014

form Extract durations from labeled segments in files
	comment Directory of sound files
	text sound_directory ./wav/
	sentence Sound_file_extension .wav
	comment Directory of TextGrid files
	text textGrid_directory ./TextGrid/
	sentence TextGrid_file_extension .TextGrid
	comment Path to save result files:
	# save results as a csv file.
	text resultpath ./duration/
	comment Which tier do you want to analyze?
	sentence Tier phone
endform

# Here, you make a listing of all the sound files in a directory.
# The example gets file names ending with ".wav" from ./Sounds/wav/

Create Strings as file list... list 'sound_directory$'*'sound_file_extension$'
numberOfFiles = Get number of strings

# Write a row with column titles to the result file:

# Go through all the sound files, one by one:
for ifile to numberOfFiles
	select Strings list
	filename$ = Get string... ifile
	
	# A sound file is opened from the listing:
	Read from file... 'sound_directory$''filename$'
	soundname$ = selected$ ("Sound", 1)
			
	# Open a TextGrid with the same name:
	gridfile$ = "'textGrid_directory$''soundname$''textGrid_file_extension$'"

	resultfile$ = "'resultpath$''soundname$'.txt"
	if fileReadable (gridfile$)
		Read from file... 'gridfile$'
		
		# Find the tier number that has the label given in the form:
		call getTier 'tier$' tier
		numberOfIntervals = Get number of intervals... tier
		
		# Pass through all intervals in the selected tier:
		for interval to numberOfIntervals
			label$ = Get label of interval... tier interval
			start = Get starting point... tier interval
			end = Get end point... tier interval					
			resultline$ = "'start''tab$''end''tab$''label$''newline$'"
			fileappend "'resultfile$'" 'resultline$'
			select TextGrid 'soundname$'
		endfor
		
		# Remove the TextGrid object from the object list
		select TextGrid 'soundname$'
		Remove
	endif
	
	# Remove the temporary objects from the object list
	select Sound 'soundname$'
	Remove
	select Strings list
	# and go on with the next sound file!
endfor

Remove

### Procedure (Subroutine)
### Get tier number with its name

procedure getTier name$ variable$
        numberOfTiers = Get number of tiers
        itier = 1
        repeat
                tier$ = Get tier name... itier
                itier = itier + 1
        until tier$ = name$ or itier > numberOfTiers
        if tier$ <> name$
                'variable$' = 0
        else
                'variable$' = itier - 1
        endif

	if 'variable$' = 0
		exit The tier called 'name$' is missing from the file 'soundname$'!
	endif
endproc