import React from 'react';
import FileChooser from './../components/fileChooser';
import ProgressBar from './../components/progressBar';
import FlashedMessages from './../components/flashedMessagesList';

export default class ParserPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {isFlushed:false, files:null, activeParsers:[], flashedMessages:[]};
    this.timer = setInterval(this.updateInfo, 1000);

    this.updateInfo()
  }

  onFileSubmit = (files) => {
    this.setState({files:files}); 
    this.startParse(files);
    this.updateInfo()
  }

  startParse = (files) => {
    const data = new FormData();
    for(var i = 0; i < files.length; i++) {
      data.append(i, files[i]);
    }

    $.ajax({
      url: '/parser/_start_parse',
      type: 'POST',
      processData: false,
      contentType: false,
      data: data 
    });
  }

  updateInfo = () => {
    this.updateProgress();
    this.updateFlashedMessages();
  }

  updateProgress = () => {
    var successFunc = this.setProgress;
    $.ajax({
      url: '/parser/_get_progress',
      type: 'POST',
      success: function(response) {
        successFunc(response);
      }
    });
  }

  updateFlashedMessages = () => {
    var successFunc = this.setFlashedMessages;
    $.ajax({
      url: '/parser/_get_flashed_messages',
      type: 'POST',
      success: function(response) {
        successFunc(response);
      }
    });
  }

  setFlashedMessages = (data) => {
    if(data) {
      var messages = this.state.flashedMessages;
      for(var key in data) {
        messages.push(data[key]) 
      }

      this.setState({flashedMessages:messages})
    }
  }

  setProgress = (data) => {
    if(data) {
      var list = [];
      for(var key in data) {
        list.push(data[key]);
      }
      this.setState({activeParsers:list});
    }
  }

  cancelTimer = () => {
    clearTimeout(this.timer);
  }

  render() {
    return(
      <div>
        <FileChooser
          onSubmit={(files) => this.onFileSubmit(files)}
        />      
        <hr/>
        <h2>Active Parse Tasks</h2>
        { this.state.activeParsers != null &&
          this.state.activeParsers.map((item) => (
            <ProgressBar
              key={item.job_id}
              progress={item.progress}
              max={item.max_progress}
              message={item.filename}
            />
          ))
        }
        <hr/>
        <FlashedMessages flashedMessages={this.state.flashedMessages}/>
      </div>
    );
  }

  componentWillUnmount() {
    console.log("unmounting");
    this.cancelTimer();
  }
} 
