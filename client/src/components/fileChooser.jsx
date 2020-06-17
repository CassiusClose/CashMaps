import React, { useState } from 'react';
import './fileChooser.css';

export default function FileChooser(props) {
  const [files, setFiles] = useState(null);

  const onSubmit = (e) => {
    e.preventDefault();
    if(props.onSubmit && files) {
      props.onSubmit(files);
    }
  }

  const onInput = (e) => {
    setFiles(e.target.files);
  }

  return(
    <div className={props.className}>
      <div className="FileChooser_Container">
        <h2 className="FileChooser_Title">{props.title}</h2>
        <p className="FileChooser_Description">{props.description}</p>
        <form className="FileChooser_Form" onSubmit={onSubmit}>
          <input className="FileChooser_FileInput"
            type="file"
            onChange={onInput}
            multiple="multiple"
            required />
          <br/>
          <input className="FileChooser_SubmitButton" type="submit" value="Submit" />
        </form>
      </div>
    </div>
  );
}

FileChooser.defaultProps = { className: "superdiv" }
