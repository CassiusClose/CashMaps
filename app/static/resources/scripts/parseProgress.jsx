class ProgressBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {show:false, progress:0, max:100};
    
  }

  updateProgress() {
    console.log(data.progress);
    console.log(data.max);
    var data = retrieveProgress();
    if(data.progress < data.max) {
      this.setState({progress:data.progress, max:data.max}); 
      this.timer = setTimeout(updateProgress, 500);
    } else {
      endProgress();
    }
  }

  startProgress() {
    alert('WOOHO');
    this.setState({show:true});
    updateProgress();
  }

  endProgress() {
    clearTimeout(this.timer);
    this.setState({show:false});
  }

  render() {
    return(
      <div>
        <React.Fragment>
          <p>Hi</p>
        </React.Fragment>
        
        <div>
        {this.state.show ? 
        
          <div>
            <hr></hr>
            <progress
              value={this.state.progress}
              max={this.state.max}
            ></progress>
          </div>

        :null
        }
        </div>
      </div>
    );
  }
}

function startProgress() {
  alert("WOWF");
}

function retrieveParserProgress(updateCallback) {
  $.ajax({
    url: '/parser/_get_progress',
    type: 'POST',
    success: function(response) {
      var data = {max: response.max, progress: response.progress};
      return data;
    }
  });
  return null;
}


var progressBar = ReactDOM.render(<ProgressBar />, document.getElementById("parseProgress"));
