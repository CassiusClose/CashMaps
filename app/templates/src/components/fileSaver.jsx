import React from 'react';

export default class FileChooser extends React.Component {
  constructor(props) {
    super(props);

    this.state = {files:null, folderpath:"", overwrite:false};
  }

  submit = (e) => {
    event.preventDefault(); //Prevent form from redirecting webpage
    if(this.props.onSubmit && this.state.files) {
      this.props.onSubmit(this.state.files, this.state.folderpath, this.state.overwrite);
    }
  }

  onFileChange = (e) => {
    this.setState({ files: e.target.files });
  }

  onFolderPathChange = (e) => {
    this.setState({ folderpath: e.target.value });
  }

  onOverwriteChange = (e) => {
    this.setState({ overwrite: e.target.checked });
  }

  render() {
    return(
      <div>
        <form onSubmit={this.submit}>
          <input
            type="file" 
            onChange={this.onFileChange} 
            multiple="multiple"
            accept={this.props.accept}
            required />
          <br/>
          Internal Folder Path:
          <input
            type="text"
            onChange={this.onFolderPathChange}
          />
          <br/>
          <input type="checkbox" onChange={this.onOverwriteChange}/>
          Overwrite?
          <br/>
          <input type="submit" value="Submit" />
          <br/>
          <div>
            {
              this.props.errors != null &&
              this.props.errors.map((item) => (
                <p style={{color:'red'}}>Error: {item}</p>
              ))
            }
          </div>
        </form>
      </div>
    );
  }
}

