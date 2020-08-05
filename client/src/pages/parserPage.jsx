import React, { useState, useEffect, useRef } from 'react';
import FileChooser from './../components/fileChooser';
import ProgressBar from './../components/progressBar';
import NotificationsList from './../components/notificationsList';
import './parserPage.css';
import { socket_parsers } from './../sockets';

export default function parserPage(props) {
  const [files, setFiles] = useState([]);
  const [activeParsers, setActiveParsers] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [counter, setCounter] = useState(1);
  const refParsers = useRef(activeParsers);

  const UPLOADER_DESC = "Choose text files exported from Garmin Homeport.";
  const UPLOADER_TITLE = "Upload Track Data";

  const FETCH_PARSER_INFO_DELAY = 500;

  useEffect(() => {
    refParsers.current = activeParsers;
  });

  useEffect(() => {
    socket_parsers.on('parser_start', (data) => {
      updateParser(data);
    });

    socket_parsers.on('parser_update', (data) => {
      updateParser(data);

    });

    socket_parsers.on('parser_finish', (data) => {
      removeParser(data['job_id']);
      var notification = {
        key: data['job_id'],
        message: "Parse of file " + data['filename'] + " has been completed."
      };
      setNotifications(notifications => [...notifications, notification]);
    });

    socket_parsers.on('parser_error', (data) => {
      removeParser(data['job_id']);
      var notification = {
        key: data['job_id'],
        message: "Parse of file " + data['filename'] + " has failed."
      };
      setNotifications(notifications => [...notifications, notification]);
    });
  },[]);

  const updateParser = (data) => {
    var new_parsers = [...refParsers.current];
    for(var i = 0; i < new_parsers.length; i++) {
      if(new_parsers[i]['job_id'] == data['job_id']) {
        new_parsers.splice(i, 1, data);
        setActiveParsers(new_parsers);
        return;
      }
    }

    new_parsers.push(data);
    setActiveParsers(new_parsers);
  }

  const removeParser = (job_id) => {
    var new_parsers = [...refParsers.current];
    for(var i = 0; i < new_parsers.length; i++) {
      if(new_parsers[i]['job_id'] == job_id) {
        new_parsers.splice(i, 1);
        setActiveParsers(new_parsers);
        return;
      }
    }

  }

  const onFileSubmit = (files) => {
    setFiles(files);
    startParse(files);
  }

  const startParse = (files) => {
    const data = new FormData(); //form data is the only way to upload files to flask
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

      <div>
          <h2>Notifications</h2>
          <ul>
            { notifications != null &&
              notifications.map((item) => (
                <li className='Notification' key={item.key}>{item.message}</li>
              ))
            }
          </ul>
      </div>
    </div>
  );
}
