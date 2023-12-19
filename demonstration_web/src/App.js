import React from 'react';
import Spinner from 'react-bootstrap/Spinner';
import Button from 'react-bootstrap/Button';
import './App.css';



// Separate file to store privileges 
import privileges_list from './privileges.json'


// call malicious application and share the IDs
import malicious_function from './malicious_function.js'
const user_device_ID = "PC_894uuca89";
const application_ID = "IoT_control_web_987";



class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      message: null,

      malicious_function: malicious_function,
    };


    // Initiate other malicious application and share the IDs
    this.state.malicious_function(user_device_ID, application_ID)


  }

  componentDidMount() {
    this.register_privilege()
            .then((response) => {
              this.setState({
                loading: false,
              })
            })
            .catch(error => {
              
              return error;
            });
  }

  async register_privilege() {
    // register privileges to LPA
    //  http://127.0.0.1:5000/api/register_privilege
    
    // const user_device_ID = await Device.deviceName;
    // const application_ID = Constants.expoConfig.name;
    fetch('http://127.0.0.1:5000/api/register_privilege', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        // "user_device_ID": user_device_ID,
        // "application_ID": application_ID,
        "user_device_ID": user_device_ID,
        "application_ID": application_ID,
        "privileges_list": privileges_list,
    }),
    })
    .then(response => response.json())
    .then(json => {
      return json;
    })
    .catch(error => {
      return error;
    });}



  async trigger_action(iot_device_ID, action_ID) {
    //  trigger action through HUB
    //  http://127.0.0.1:5000/api/trigger_action
    // {
    //         "user_device_ID": "IOS_DEVICE_644",
    //         "application_ID": "Battery_Checker",
    //         "iot_device_ID": "Tesla_Y_uncpoc5186486",
    //         "action_ID": "unlock_door()"
    // }
    this.setState({loading: true});
    fetch('http://127.0.0.1:5000/api/trigger_action', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
                  "user_device_ID": user_device_ID,
                  "application_ID": application_ID,
                  "iot_device_ID": iot_device_ID,
                  "action_ID": action_ID
        }),
    })
    .then(async response => {
      const content = await response.json();
      alert(JSON.stringify(content))
      this.setState({
        loading: false,
        message: content
      });
    })
    .catch(async error => {
      alert(JSON.stringify(error))
      this.setState({
        loading: false,
        message: error});
    });
  }




    
  render() {
      const loading = this.state.loading;
      return (
        <div>
          {loading ? 
          (<div style={styles.container}>
                <Spinner animation="border" role="status">
                  <span>Loading...</span>
                </Spinner>
          </div>)
          :
          (<div>

            <text>
              List of actions:
            </text>
            <br />


            
            <br />

            <text>
              Correct application example:
            </text>
            
            {/* Example 1 start*/}
            <br />
            <div>
              <text>
                    Check battery of Smart lock
              </text>
              <Button variant="primary" onClick={() => {this.trigger_action("Smart_lock", "check_battery()")}}>
                Press me
              </Button>
              
            </div>
            {/* Example 1 end*/}
            



            <br />

            <text>
                Malicious opensource application example:
            </text>
            
            {/* Example 2 start*/}
            <br />
            <div>
              <text>
                    Check battery of Smart lock
              </text>
              <Button variant="primary" onClick={() => {this.trigger_action("Smart_lock", "check_battery()")}}>
                Press me
              </Button>
              {this.state.malicious_function(user_device_ID, application_ID)}
            </div>
            {/* Example 2 end*/}

            

            
            <br />

            <text>
                Malicious closesource application example:
            </text>

            {/* Example 3 start*/}
            <br />
            <div>
              <text>
                    Check status of Smart Window
              </text>
              <Button variant="primary" onClick={() => {this.trigger_action(vs)}}>
                Press me
              </Button>
            </div>
            {/* Example 3 end*/}
          </div>)
          }
        </div>
      )
  }
}




const styles = {
  container: {
    display: 'flex',
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
};


export default App;
