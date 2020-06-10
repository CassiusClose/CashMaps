import React, { useState, useEffect } from 'react';
//import io from 'socket.io';
import FileChooser from './../components/fileChooser';
import ProgressBar from './../components/progressBar';
import FlashedMessages from './../components/flashedMessagesList';
import NotificationsList from './../components/notificationsList';
import './parserPage.css';

export default function parserPage(props) {
  const [files, setFiles] = useState([]);
  const [activeParsers, setActiveParsers] = useState([]);
  const [counter, setCounter] = useState(1);

  const UPLOADER_DESC = "Choose text files exported from Garmin Homeport.";
  const UPLOADER_TITLE = "Upload Track Data";

  const FETCH_PARSER_INFO_DELAY = 500;

  useEffect(() => {
    console.log('fetching...');
    var scheduler = setTimeout(() => {
      $.ajax({
        url: '/parser/_get_progress',
        type: 'POST',
        success: function(response) {
          console.log("receieved");
          if(response.tasks) {
            setActiveParsers([...response.tasks]);
            setCounter((counter+1)%100);
          }
        }
      });
    }, FETCH_PARSER_INFO_DELAY);

    return () => {
      clearTimeout(scheduler);
    };
  })

  const onFileSubmit = (files) => {
    setFiles(files);
    startParse(files);
  }

  const startParse = (files) => {
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

  return(
    <div className="ParserPage_Container">
      <div className="ParserPage_Row1">
        <FileChooser
          className="ParserPage_Uploader"
          onSubmit={(files) => onFileSubmit(files)}
          title={UPLOADER_TITLE}
          description={UPLOADER_DESC}
        />      

        <div className="ParserPage_Progress">
          <h2>Active Parse Tasks</h2>
          { activeParsers != null &&
            activeParsers.map((item) => (
              <ProgressBar
                key={item.job_id}
                progress={item.progress} max={item.max_progress}
                message={item.filename}
              />
            ))
          }
        </div>
      </div>
      
      <NotificationsList notification_name="parse"/>
    </div>
  );
}
//<FlashedMessages url="/parser/_get_flashed_messages"/>
