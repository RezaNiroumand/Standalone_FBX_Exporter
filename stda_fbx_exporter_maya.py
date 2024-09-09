import sys
import os
import argparse
import ast
import maya.standalone
import maya.cmds as cmds

# top most rig joint.
ROOT_JOINT = 'root_jj'

# Function to initialize Maya standalone
def initialize_maya_standalone():
    try:
        maya.standalone.initialize(name='python')
        print("Maya standalone initialized successfully.")
    except Exception as e:
        print(f"Error initializing Maya standalone: {e}")
        sys.exit(1)

# Function to check and print environment variables
def check_environment_variables(var_names):
    for var_name in var_names:
        value = os.environ.get(var_name)
        if value is not None:
            print(f"{var_name} = {value}")
        else:
            print(f"{var_name} is not set.")

# load 
def load_plugin(plugin_name, load):
    # load plugins
    if load == True:
        cmds.loadPlugin(plugin_name)
        return
    if load == False:
        cmds.unloadPlugin(plugin_name)

def check_plugin_loaded(plugin_name):
    is_loaded = cmds.pluginInfo(plugin_name, query=True, loaded=True)
    if is_loaded:
        print(f"The plugin '{plugin_name}' is loaded.")
    else:
        print(f"The plugin '{plugin_name}' is not loaded.")
    return is_loaded

def parse_list(string):
    try:
        return ast.literal_eval(string)
    except (ValueError, SyntaxError) as e:
        raise argparse.ArgumentTypeError(f"Invalid list format: {string}")

def stda_fbx_exporter_with_options(start_frame, end_frame, scene_fps, file_path, object, includeChildren, inputConnections):
    # local variables with values
    is_animation = 1
    frame_step = 1
    deformation = 1
    deformation_skins = 1
    deformation_blend_shapes = 1
    fbx_format_type = 'Binary'

    
    #fbx properties
    cmds.FBXProperty('Export|IncludeGrp|Animation', '-v', is_animation)
    cmds.FBXProperty('Export|AdvOptGrp|Collada|FrameRate', '-v', scene_fps)

    cmds.FBXProperty('Export|IncludeGrp|Animation|BakeComplexAnimation', '-v', 1)
    cmds.FBXProperty('Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameStart', '-v', start_frame)
    cmds.FBXProperty('Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameEnd', '-v', end_frame)
    cmds.FBXProperty('Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameStep', '-v', frame_step)
    cmds.FBXProperty('Export|IncludeGrp|Animation|Deformation', '-v', deformation)
    cmds.FBXProperty('Export|IncludeGrp|Animation|Deformation|Skins', '-v', deformation_skins)
    cmds.FBXProperty('Export|IncludeGrp|Animation|Deformation|Shape', '-v', deformation_blend_shapes)
    cmds.FBXProperty('Export|IncludeGrp|InputConnectionsGrp|IncludeChildren', '-v', includeChildren)
    cmds.FBXProperty('Export|IncludeGrp|InputConnectionsGrp|InputConnections', '-v', inputConnections)
    cmds.FBXProperty('Export|AdvOptGrp|Fbx|AsciiFbx', '-v', fbx_format_type)
    
    cmds.FBXProperty('Export|AdvOptGrp|UI|GenerateLogData', '-v', 1)
    
    #export
    selected_object = object
    cmds.select(selected_object, replace=True)
    cmds.FBXExport("-file", file_path, "-s")

    print(file_path)
    print('stda_fbx_exporter_with_options successful')

def get_scene_directory():
    file_name = os.path.basename(cmds.file(q=True, sn=True))

    scene_file_path = cmds.file(q=True, sceneName=True)

    scene_directory = os.path.dirname(scene_file_path)

    project_path = cmds.workspace(query=True, rootDirectory=True)

    return file_name, scene_file_path, scene_directory, project_path

def find_top_most_parent(obj):
    parents = cmds.listRelatives(obj, parent=True, fullPath=True)
    if parents:
        return find_top_most_parent(parents[0])
    else:
        return obj

def find_objects_with_suffix(suffix):
    # List all objects in the scene
    all_objects = cmds.ls(dag=True, long=True)

    # Filter objects that end with the given suffix
    matching_objects = [obj for obj in all_objects if obj.endswith(suffix)]

    return matching_objects

def find_objects_with_namespace(suffix):
    # List all objects in the scene
    all_objects = cmds.ls(dag=True, long=False)

    # Filter objects that end with the given suffix
    matching_objects = [obj for obj in all_objects if obj.endswith(suffix)]
    
    return matching_objects

def get_object_namespaces():
    # Define the suffix
    suffix = ROOT_JOINT
    
    # Find objects with the specified suffix
    matching_objects = find_objects_with_namespace(suffix)

    # Find and print the top-most parent for each matching object
    if matching_objects:
        for obj in matching_objects:
            split_obj = obj.split(':')
        split_obj.remove(suffix)
        return split_obj
    return 0

def remove_namespace(list_of_namespace):
	namespaces = list_of_namespace
	for ns in namespaces:
		cmds.namespace(removeNamespace=ns, mergeNamespaceWithRoot=True)

def strip_namespace(obj):
    return obj.split(':')[-1]

def get_root_joint_top_parent():
    # Define the suffix
    suffix = ROOT_JOINT
    
    # Find objects with the specified suffix
    matching_objects = find_objects_with_suffix(suffix)
    
    # Find and print the top-most parent for each matching object
    if matching_objects:
        for obj in matching_objects:
            top_most_parent = find_top_most_parent(obj)
            stripped_obj = strip_namespace(obj)
            stripped_top_most_parent = strip_namespace(top_most_parent)
            stripped_top_most_parent_rngroup = stripped_top_most_parent.replace('|', '').replace('RNgroup', '')
            # print(f"Object matching suffix '{suffix}': {stripped_obj}")
            # print(f"Top-most parent: {stripped_top_most_parent}")
            return stripped_top_most_parent_rngroup
    
    print(f"No objects found with suffix '{suffix}'")
    return 0

def get_list_set_members():
    # get list of sets in scene
    object_sets = cmds.ls(type='objectSet')
    anim_export_set = [set for set in object_sets if set.endswith('Anim_Export')]
    return anim_export_set

# Main function
def main():
    parser = argparse.ArgumentParser(description= 'Specify the maya file to open')
    parser.add_argument('-mf',
                        '--maya_file',
                        help= 'User specify which maya file to open',
                        type = str,
                        required = True)
    args = parser.parse_args()

    #  maya standalone
    initialize_maya_standalone()
    #-------------------------------------------------#
    '''
    First Export to export sets_to_select
    '''
    #-------------------------------------------------#
    # open new empty scene
    cmds.file(new=True, force=True)
    # load fbx

    load_plugin('fbxmaya', True)
    check_plugin_loaded('fbxmaya')
    check_plugin_loaded('xgenToolkit')
    
    # open scene file
    print(args.maya_file)
    cmds.file(args.maya_file, o=True)

    # query this varaible after maya is opened
    # change file name as per requirements, the file name is set to look for the object top transform name for ease of creating this script. 
    # file_name = get_root_joint_top_parent() + '_stda_fbx' # < change file name if needed
    # print(file_name)
    
    # scene directory can be set to project based directory
    # get_scene_directory[2] function will return file directory for ease of creating this script.
    scene_directory = get_scene_directory()[2]
    print(scene_directory)

    
    # get the namesapce to concat with 'Anim_Export' then prep for removal in second export
    obj_namespaces = get_object_namespaces()

    # 'Anim_Export is the set in maya to look for for this FBX export. can be changed as per requirements'
    sets_to_select = get_list_set_members()
    # sets_to_select = cmds.sets(obj_namespaces[0] + ':Anim_Export', q=True) # < change if set name is not 'Anim Export'
    start_frame = cmds.playbackOptions(query=True, minTime=True)
    end_frame = cmds.playbackOptions(query=True, maxTime=True)
    fps = cmds.playbackOptions(query=True, framesPerSecond=True)

    file_paths = []
    for set in sets_to_select:
        print('printing set')
        print(set)
        # concat dir and file name
        file_name = set.split(':')
        file_path_for_export = '{0}/{1}.fbx'.format(scene_directory, file_name[-2]) # -2 for the last namespace
        file_paths.append(file_path_for_export)
        stda_fbx_exporter_with_options(start_frame, end_frame, fps, file_path_for_export, set, 0, 0)

    for path in file_paths:
        #-------------------------------------------------#
        '''
        Second Export to clean up, grouping and namespace
        '''
        #-------------------------------------------------#
        # open clean maya again..
        cmds.file(new=True, force=True)
        # import fbx
        cmds.file(path, i=True, type='FBX', ra=True, mergeNamespacesOnClash=False, options="fbx")
    
        # 1. get the namespace to concat with 'Anim_Export' 
        # 2. prep for removal in second export
        obj_namespaces = get_object_namespaces()
        print(obj_namespaces)
        
        # remove namespaces
        if obj_namespaces:
            remove_namespace(obj_namespaces)
            print('Namespace removed')
        else:
            print("No namespaces found")
        
        # unparent ROOT_JOINT and export
        cmds.parent(ROOT_JOINT, world=True)
        stda_fbx_exporter_with_options(start_frame, end_frame, fps, path, ROOT_JOINT, 1, 0)

    print("Script ran successfully. Unintializing standalone maya!")
    # Uninitialize Maya standalone
    maya.standalone.uninitialize()

    # os.startfile(scene_directory)

if __name__ == '__main__':
    main() 
