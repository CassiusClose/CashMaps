import React from 'react';
import './fileChooser.css';

export default class FileChooser extends React.Component {
  constructor(props) {
    super(props);

    var superdiv = "superdiv";
    if(props.className != null) {
      superdiv = props.className;
    }

    this.state = {files:null, className:props.className};
  }

  submit = (e) => {
    event.preventDefault(); //Prevent form from redirecting webpage
    if(this.props.onSubmit && this.state.files) {
      this.props.onSubmit(this.state.files);
    }
  }

  onInput = (e) => {
    this.setState({ files: e.target.files });
  }

  render() {
    return(
      <div className={this.state.className}>
        <div className="FileChooser_Container">
          <h2 className="FileChooser_Title">{this.props.title}</h2>
          <p className="FileChooser_Description">{this.props.description}</p>
          <form className="FileChooser_Form" onSubmit={this.submit}>
            <input className="FileChooser_FileInput" type="file" onChange={this.onInput} multiple="multiple"
              required />
            <br/>
            <input className="FileChooser_SubmitButton" type="submit" value="Submit" />
          </form>
        </div>
      </div>
    );
  }
}
