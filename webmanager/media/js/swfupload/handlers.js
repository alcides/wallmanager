function fileQueueError(file, errorCode, message)  {
	try {
		// Handle this error separately because we don't want to create a FileProgress element for it.
		switch (errorCode) {
		case SWFUpload.QUEUE_ERROR.QUEUE_LIMIT_EXCEEDED:
			alert("You have attempted to queue too many files.\n" + (message === 0 ? "You have reached the upload limit." : "You may select " + (message > 1 ? "up to " + message + " files." : "one file.")));
			return;
		case SWFUpload.QUEUE_ERROR.FILE_EXCEEDS_SIZE_LIMIT:
			alert("The file you selected is too big.");
			this.debug("Error Code: File too big, File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
			return;
		case SWFUpload.QUEUE_ERROR.ZERO_BYTE_FILE:
			alert("The file you selected is empty.  Please select another file.");
			this.debug("Error Code: Zero byte file, File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
			return;
		case SWFUpload.QUEUE_ERROR.INVALID_FILETYPE:
			alert("The file you choose is not an allowed file type.");
			this.debug("Error Code: Invalid File Type, File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
			return;
		default:
			alert("An error occurred in the upload. Try again later.");
			this.debug("Error Code: " + errorCode + ", File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
			return;
		}
	} catch (e) {
	}
}

function uploadProgress(file, bytesLoaded, bytesTotal) {

	try {
		var percent = Math.ceil((bytesLoaded / bytesTotal) * 100);

		file.id = "singlefile";	// This makes it so FileProgress only makes a single UI element, instead of one for each file
		var progress = new FileProgress(file, this.customSettings.progress_target);
		progress.setProgress(percent);
		progress.setStatus("Uploading...");
	} catch (e) {
	}
}

function uploadSuccess(file, serverData) {
	file.id = "singlefile";	// This makes it so FileProgress only makes a single UI element, instead of one for each file
	var progress = new FileProgress(file, this.customSettings.progress_target);
	progress.setComplete();
	progress.setStatus("Complete.");
	progress.toggleCancel(false);
	
	if (serverData === " ") {
		this.customSettings.upload_successful = false;
	} else {
		this.customSettings.upload_successful = true;
		document.getElementById("hidFileID").value = serverData;
	}
}

function uploadComplete(file) {
	if (this.customSettings.upload_successful) {
		this.setButtonDisabled(true);
		uploadDone();
	} else {
		file.id = "singlefile";	// This makes it so FileProgress only makes a single UI element, instead of one for each file
		var progress = new FileProgress(file, this.customSettings.progress_target);
		progress.setError();
		progress.setStatus("File rejected");
		progress.toggleCancel(false);
		
		var txtFileName = document.getElementById("hidFileID");
		txtFileName.value = "";

		alert("There was a problem with the upload.\nThe server did not accept it.");
	}
}

function uploadError(file, errorCode, message) {

	if (errorCode === SWFUpload.UPLOAD_ERROR.FILE_CANCELLED) {
		// Don't show cancelled error boxes
		return;
	}
	
	// Handle this error separately because we don't want to create a FileProgress element for it.
	switch (errorCode) {
	case SWFUpload.UPLOAD_ERROR.MISSING_UPLOAD_URL:
		alert("There was a configuration error.  You will not be able to upload a resume at this time.");
		this.debug("Error Code: No backend file, File name: " + file.name + ", Message: " + message);
		return;
	case SWFUpload.UPLOAD_ERROR.UPLOAD_LIMIT_EXCEEDED:
		alert("You may only upload 1 file.");
		this.debug("Error Code: Upload Limit Exceeded, File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
		return;
	case SWFUpload.UPLOAD_ERROR.FILE_CANCELLED:
	case SWFUpload.UPLOAD_ERROR.UPLOAD_STOPPED:
		break;
	default:
		alert("An error occurred in the upload. Try again later.");
		this.debug("Error Code: " + errorCode + ", File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
		return;
	}

	file.id = "singlefile";	// This makes it so FileProgress only makes a single UI element, instead of one for each file
	var progress = new FileProgress(file, this.customSettings.progress_target);
	progress.setError();
	progress.toggleCancel(false);

	switch (errorCode) {
	case SWFUpload.UPLOAD_ERROR.HTTP_ERROR:
		progress.setStatus("Upload Error");
		this.debug("Error Code: HTTP Error, File name: " + file.name + ", Message: " + message);
		break;
	case SWFUpload.UPLOAD_ERROR.UPLOAD_FAILED:
		progress.setStatus("Upload Failed.");
		this.debug("Error Code: Upload Failed, File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
		break;
	case SWFUpload.UPLOAD_ERROR.IO_ERROR:
		progress.setStatus("Server (IO) Error");
		this.debug("Error Code: IO Error, File name: " + file.name + ", Message: " + message);
		break;
	case SWFUpload.UPLOAD_ERROR.SECURITY_ERROR:
		progress.setStatus("Security Error");
		this.debug("Error Code: Security Error, File name: " + file.name + ", Message: " + message);
		break;
	case SWFUpload.UPLOAD_ERROR.FILE_CANCELLED:
		progress.setStatus("Upload Cancelled");
		this.debug("Error Code: Upload Cancelled, File name: " + file.name + ", Message: " + message);
		break;
	case SWFUpload.UPLOAD_ERROR.UPLOAD_STOPPED:
		progress.setStatus("Upload Stopped");
		this.debug("Error Code: Upload Stopped, File name: " + file.name + ", Message: " + message);
		break;
	}
}