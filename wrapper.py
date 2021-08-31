import sys
from subprocess import call
from argparse import ArgumentParser
import json

def main(argv):
    with open('/app/descriptor.json') as f:
        data = json.load(f)

    inputs = data['inputs']
    targetParams = {}
    descriptions = {}
    params = {}
    
    for input in inputs:
        key = input['id'].replace('ij_', '')
        value = input['default-value']
        description = input['description']
        targetParams[key] = value
        descriptions[key] = description
        params[key] = input['id']
        
    infolder = "/data/in"
    outfolder = "/data/out"
    
    parser = ArgumentParser(description='Parse the input and output folder options and the options for the workflow.')
    parser.add_argument("--infolder", dest="input", default=infolder, required=False,
                              help="Absolute path to the container folder where the input data to be processed is "
                                   "stored. If not specified, a custom folder is created and used by the workflow.")    
    parser.add_argument("--outfolder", dest="output", default=outfolder, required=False,
                              help="Absolute path to the container folder where the output data will be generated."
                                   "If not specified, a custom folder is created and used by the workflow.")
    for key,value in params.items():
           parser.add_argument("--" + value, dest=key, default=targetParams[key] , required=False, help=descriptions[key])
    args = parser.parse_args(argv)
    
    for arg in vars(args):
        if not arg is "infolder" and not arg is outfolder:
            targetParams[arg] = getattr(args, arg)
    
    command = "/usr/bin/xvfb-run java -Xmx6000m -cp /fiji/jars/ij.jar ij.ImageJ --headless --console " \
          "-macro macro.ijm \""
    isFirst = True
    for param in targetParams.keys():
        if not isFirst:
            command = command + ", "
        command = command + param + "={}"      
        isFirst = False
    command = command + "\"" 
    command = command.format(*list(targetParams.values()))     
    
    print('Running command: ' + command)
    
    return_code = call(command, shell=True, cwd="/fiji")  # waits for the subprocess to return

    if return_code != 0:
        err_desc = "Failed to execute the ImageJ macro (return code: {})".format(return_code)
        raise ValueError(err_desc)
    else:
        print("Workflow executed successfully.")
 

if __name__ == "__main__":
    main(sys.argv[1:])
