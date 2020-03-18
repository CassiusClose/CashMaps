import React from 'react';
import FileSaver from './../components/fileSaver';
import FlashedMessages from './../components/flashedMessagesList';
var path = require('path');

export default class UploadPage extends React.Component {
  constructor(props) {
    super(props);

    //TODO Should this be in the FileSaver component?
    this.state = {'acceptedExts': ['.jpg', '.png'], uploadErrors: [], flashedMessages:[]}

    this.timer = setInterval(this.updateStatus, 2000);
  }

  updateStatus = () => {
    this.getFlashedMessages();
  }

  submitForm = (files, folderpath, overwrite) => {
    this.clearFlashedMessages();

    this.uploadFiles(files, folderpath, overwrite);
  }

  getFlashedMessages = () => {
    var successFunc = this.setFlashedMessages
    $.ajax({
      url: '/_get_upload_flashed_messages',
      type: 'POST',
      success: function(response) {
        successFunc(response.messages);
      }
    });
  }

  setFlashedMessages = (data) => {
    if(data.length > 0) {
      this.setState({flashedMessages:data});
    }
  }

  clearFlashedMessages = () => {
    this.setState({flashedMessages:[]});
  }

  uploadFiles = (files, folderpath, overwrite) => {
    var data = new FormData();
    for(var i = 0; i < files.length; i++) {
      data.append(i, files[i]);
    }
    data.append('filepath', folderpath);
    data.append('overwrite', overwrite);

    $.ajax({
      url: '/_upload_photo',
      type: "POST",
      processData: false,
      contentType: false,
      data: data
    });
  }

  cancelTimer = () => {
    clearTimeout(this.timer);
  }

  addError = (message) => {
    var errors = this.state.uploadErrors;
    errors.push(message);
    this.setState({uploadErrors: errors});
  }

  clearErrors = () => {
    this.setState({'uploadErrors':[]})
  }
  
  render() {
    return (
      <div>
        <FileSaver
          onSubmit={this.submitForm}
          errors={this.state.uploadErrors}
          accept={"image/*"}
        />
        <FlashedMessages
          flashedMessages = {this.state.flashedMessages}
        />
      </div>
    );
  }

  /** Cleans up after the component when it's being unmounted. */
  componentWillUnmount() {
    this.cancelTimer(); //Cancels the status update timer
  }
}
