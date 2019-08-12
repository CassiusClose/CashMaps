import React from 'react';

export default class FileChooser extends React.Component {
  constructor(props) {
    super(props);

    this.state = {files:null};
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
      <div>
        <form onSubmit={this.submit}>
          <input
            type="file" 
            onChange={this.onInput} 
            multiple="multiple"
            required />
          <br/>
          <input type="submit" value="Submit" />
        </form>
      </div>
    );
  }
}
