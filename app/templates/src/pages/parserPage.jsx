import React from 'react';
import FileChooser from './../components/fileChooser';
import ProgressBar from './../components/progressBar';
import FlashedMessages from './../components/flashedMessagesList';
import './parserPage.css';

/**
 * Provides the user with a way to parse track file data and displays info on active parsing jobs.
 */
export default class ParserPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = { files:null,           //Files selected by the <input> tag
      activeParsers:[],     //Active parse jobs, JSON dictionaries read into <progress> tags
      flashedMessages:[],    //Any messages from the server, displayed on the page
      uploaderDescription: "Choose text files exported from Garmin Homeport.",
      uploaderTitle: "Upload Track Data",
    };
    this.timer = setInterval(this.updateInfo, 1000); //Repeatedly poll for status updates

    this.updateInfo() //Poll for updates now, don't wait for the timer to finish its first delay
  }

  /** Handles a submit of the file input form, uploading the files to the server to parse and
   * polling for status updates. */
  onFileSubmit = (files) => {
    this.setState({files:files}); 
    this.startParse(files);
    this.updateInfo()
  }

  /** Uploads the files to the server to be parsed. */
  startParse = (files) => {
    const data = new FormData(); //Form data is the only way to upload files to flask
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

  /** Poll for updates on active parse jobs and new flashed messages. */
  updateInfo = () => {
    this.updateProgress();
    this.updateFlashedMessages();
  }

  /** Get active parse job info from the server and pass it to setProgress(). */
  updateProgress = () => {
    var successFunc = this.setProgress;
    $.ajax({
      url: '/parser/_get_progress',
      type: 'POST',
      success: function(response) {
        successFunc(response.tasks);
      }
    });
  }

  /** Get new flashed messages from the server and pass them to setFlashedMessages(). */
  updateFlashedMessages = () => {
    var successFunc = this.setFlashedMessages;
    $.ajax({
      url: '/parser/_get_flashed_messages',
      type: 'POST',
      success: function(response) {
        successFunc(response.messages);
      }
    });
  }

  /** Adds new flashed messages to the existing array of messages. */
  setFlashedMessages = (data) => {
    if(data) {
      //Get copy of existing list and add to it. Then resubmit it to the state so that
      //existing flashed messages aren't removed until the page unloads
      var messages = this.state.flashedMessages.concat(data);
      this.setState({flashedMessages:messages})
    }
  }

  /** Updates the state's list of active parsers. */
  setProgress = (data) => {
    if(data) {
      var list = [].concat(data);
      this.setState({activeParsers:list});
    }
  }

  /** Cancels the timer that gets status updates. Should be called when unloading the page. */
  cancelTimer = () => {
    clearTimeout(this.timer);
  }

  render() {
    return(
      <div className="ParserPage_Container">
        <div className="ParserPage_Row1">
          <FileChooser
            className="ParserPage_Uploader"
            onSubmit={(files) => this.onFileSubmit(files)}
            title={this.state.uploaderTitle}
            description={this.state.uploaderDescription}
          />      

          <div className="ParserPage_Progress">
            <h2>Active Parse Tasks</h2>
            { this.state.activeParsers != null &&
              this.state.activeParsers.map((item) => (
                <ProgressBar
                  key={item.job_id}
                  progress={item.progress} max={item.max_progress}
                  message={item.filename}
                />
              ))
            }
          </div>
        </div>

        <FlashedMessages flashedMessages={this.state.flashedMessages}/>
      </div>
    );
  }

  /** Cleans up after the component when it's being unmounted. */
  componentWillUnmount() {
    this.cancelTimer(); //Cancels the status update timer
  }
} 
