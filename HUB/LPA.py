from flask import Flask, jsonify, request
from utils import *
from flask_cors import CORS
app = Flask(__name__)
CORS(app)



@app.route('/api/register_privilege', methods=['POST'])
def register_privilege():
    """
        register privilege to LPA
        ONLY allowed to register once for each user_device_ID and application_ID
    """
    try:
        privileges = request.get_json()
            # privileges : {
            #   "user_device_ID": user_device_ID,
            #   "application_ID": application_ID,
            #   "privileges_list": [ {
            #                      "iot_device_ID": iot_device_ID,
            #                      "action_ID": action_ID
            #                       },...]
            # }
        
        # each user_device_ID and application_ID can only register once
        is_registered, error = is_user_device_appliction_registered(privileges['user_device_ID'], privileges['application_ID'])
        if error != None:
            return jsonify({
                            "error": str(error), 
                            }), 400
        if is_registered:
            error_str = "user_device_ID: {}, application_ID: {} already registered"
            error_str = error_str.format(privileges['user_device_ID'], privileges['application_ID'])
            return jsonify({
                            "error": error_str,
                            }), 400
        # register
        privileges_list = privileges['privileges_list']
        for privilege_dict in privileges_list:
            add_privilege(privileges['application_ID'], privilege_dict['iot_device_ID'], privileges['user_device_ID'], privilege_dict['action_ID'])
        
        return jsonify({
                        "status": "success", 
                        }), 200
    except Exception as e:
        return jsonify({
                        "error": str(e), 
                        }), 400
        
        
@app.route('/api/remove_privilege', methods=['POST'])
def rm_privilege():
    """
        remove privilege from LPA, only the root user can remove privileges
        NOT intended to be called by application, only for testing purposes
    """
    
    try:
        privileges = request.get_json()
            # privileges : {
            #   "user_device_ID": user_device_ID,
            #   "application_ID": application_ID,
            #   "privileges_list": [ {
            #                      "iot_device_ID": iot_device_ID,
            #                      "action_ID": action_ID
            #                       },...]
            # }
        
        remove_privilege(privileges["application_ID"], privileges["user_device_ID"])
        return jsonify({
                        "status": "success", 
                        }), 200
    except Exception as e:
        return jsonify({
                        "error": str(e), 
                        }), 400
    
    
@app.route('/api/is_privileged', methods=['GET'])
def is_privileged():
    """
        return whether the privilege is granted or not from LPA
    """
    request_json = request.get_json()
    try:
        is_privileged, error = get_privilege(request_json['application_ID'], request_json['iot_device_ID'], request_json['user_device_ID'], request_json['action_ID'])
        if error == None:
            return jsonify({
                            "is_privileged": is_privileged, 
                            }), 200
        else:
            return jsonify({
                            "error": str(error), 
                            }), 400
    except Exception as e:
        return jsonify({
                        "error": str(e), 
                        }), 400

@app.route('/api/trigger_action', methods=['POST'])
def trigger_action():
    """
        trigger action of devices if LPA grant its privilege
    """
    request_json = request.get_json()
    try:
        is_privileged, error = get_privilege(request_json['application_ID'], request_json['iot_device_ID'], request_json['user_device_ID'], request_json['action_ID'])
        if error == None:
            if is_privileged == True:
                # trigger action
                
                trigger_iot_device_action(request_json['iot_device_ID'], request_json['action_ID'])
                
                return jsonify({
                                "status": "success", 
                                }), 200
            else:
                error_str = "user_device_ID: {}, application_ID: {}, does not have privilege on iot_device_ID: {}, action_ID: {}"
                error_str = error_str.format(request_json['user_device_ID'], request_json['application_ID'], request_json['iot_device_ID'], request_json['action_ID'])
                return jsonify({
                                "error": error_str,
                                }), 400
        else:
            return jsonify({
                            "error": str(error), 
                            }), 400
    except Exception as e:
        return jsonify({
                        "error": str(e), 
                        }), 400



if __name__ == '__main__':
    create_database()
    app.run(debug=True)