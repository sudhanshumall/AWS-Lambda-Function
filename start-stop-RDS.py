import boto3
import traceback

rds = boto3.client('rds')

def lambda_handler(event, context):

    try:
              
        start_stop_rds_instances(event, context)
        
    except Exception as e:
            displayException(e)
            traceback.print_exc()
            

def start_stop_rds_instances(event, context):

    # Get action parameter from event
    action = event.get('action')

    if action is None:
        action = ''

    # Check action
    if action.lower() not in ['start', 'stop']:
        print ("action was neither start nor stop. start_stop_rds_instances aborted.")
    else:
        # Get all of rds instances
        instances_rds = rds.describe_db_instances().get('DBInstances', [])
    
        print ("Found " + str(len(instances_rds)) + " RDS instances")
    
        # Loop through instances
        for instance_rds in instances_rds:

            try:
                instance_state = instance_rds['DBInstanceStatus']
                instance_id = instance_rds['DBInstanceIdentifier']

                # Get rds instance tags
                tags = rds.list_tags_for_resource(ResourceName = instance_rds['DBInstanceArn']).get('TagList',[])

                for tag in tags:
                    # Filter instances based on tag
                    if tag['Key'] == 'Auto-StartStop-Enabled':
        
                        print ("Current instance_state of %s is %s" % (instance_id, instance_state))
                
                        # Start or stop instance
                        if instance_state == 'available' and action == 'stop':
                            rds.stop_db_instance(
                                DBInstanceIdentifier = instance_id,
                                # DryRun = True
                            )
                            print ("Instance %s comes to stop" % instance_id)
                    
                        elif instance_state == 'stopped' and action == 'start':
                            rds.start_db_instance(
                                DBInstanceIdentifier = instance_id,
                                # DryRun = True
                            )
                            print ("Instance %s comes to start" % instance_id)
                            
                        else:
                            print ("Instance %s status is not right to start or stop" % instance_id)
                            
            except Exception as e:
                displayException(e)
                # traceback.print_exc()
            

def displayException(exception):
    exception_type = exception.__class__.__name__ 
    exception_message = str(exception) 

    print("Exception type: %s; Exception message: %s;" % (exception_type, exception_message))
