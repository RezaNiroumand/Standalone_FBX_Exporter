import re


fbx_properties = """
# PATH: Import|PlugInGrp|PlugInUIWidth    ( TYPE: Integer ) ( VALUE: 500 ) # 
# PATH: Import|PlugInGrp|PlugInUIHeight    ( TYPE: Integer ) ( VALUE: 500 ) # 
# PATH: Import|PlugInGrp|PlugInUIXpos    ( TYPE: Integer ) ( VALUE: 100 ) # 
# PATH: Import|PlugInGrp|PlugInUIYpos    ( TYPE: Integer ) ( VALUE: 100 ) # 
# PATH: Import|PlugInGrp|UILIndex    ( TYPE: Enum )  ( VALUE: "ENU" )  (POSSIBLE VALUES: "ENU" "DEU" "FRA" "JPN" "KOR" "CHS" "PTB"  ) # 
# PATH: Import|IncludeGrp|MergeMode    ( TYPE: Enum )  ( VALUE: "Add and update animation" )  (POSSIBLE VALUES: "Add" "Add and update animation" "Update animation"  ) # 
# PATH: Import|IncludeGrp|Geometry|UnlockNormals    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Import|IncludeGrp|Geometry|HardEdges    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Import|IncludeGrp|Geometry|BlindData    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|IncludeGrp|Animation    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|IncludeGrp|Animation|ExtraGrp|Take    ( TYPE: Enum )  ( VALUE: "No Animation" )  (POSSIBLE VALUES: "No Animation"  ) # 
# PATH: Import|IncludeGrp|Animation|ExtraGrp|TimeLine    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Import|IncludeGrp|Animation|ExtraGrp|BakeAnimationLayers    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|IncludeGrp|Animation|ExtraGrp|Markers    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Import|IncludeGrp|Animation|ExtraGrp|Quaternion    ( TYPE: Enum )  ( VALUE: "Resample As Euler Interpolation" )  (POSSIBLE VALUES: "Retain Quaternion Interpolation" "Set As Euler Interpolation" "Resample As Euler Interpolation"  ) # 
# PATH: Import|IncludeGrp|Animation|ExtraGrp|ProtectDrivenKeys    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Import|IncludeGrp|Animation|ExtraGrp|DeformNullsAsJoints    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|IncludeGrp|Animation|ExtraGrp|NullsToPivot    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|IncludeGrp|Animation|ExtraGrp|PointCache    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|IncludeGrp|Animation|Deformation    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|IncludeGrp|Animation|Deformation|Skins    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|IncludeGrp|Animation|Deformation|Shape    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|IncludeGrp|Animation|Deformation|ForceWeightNormalize    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Import|IncludeGrp|Animation|SamplingPanel|SamplingRateSelector    ( TYPE: Enum )  ( VALUE: "Scene" )  (POSSIBLE VALUES: "Scene" "File" "Custom"  ) # 
# PATH: Import|IncludeGrp|Animation|SamplingPanel|CurveFilterSamplingRate    ( TYPE: Number ) ( VALUE: 30.000000 ) # 
# PATH: Import|IncludeGrp|Animation|CurveFilter    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Import|IncludeGrp|Animation|ConstraintsGrp|Constraint    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Import|IncludeGrp|Animation|ConstraintsGrp|CharacterType    ( TYPE: Enum )  ( VALUE: "HumanIK" )  (POSSIBLE VALUES: "None" "HumanIK"  ) # 
# PATH: Import|IncludeGrp|CameraGrp|Camera    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|IncludeGrp|LightGrp|Light    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|IncludeGrp|Audio    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|UnitsGrp|DynamicScaleConversion    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|UnitsGrp|UnitsSelector    ( TYPE: Enum )  ( VALUE: "Millimeters" )  (POSSIBLE VALUES: "Millimeters" "Centimeters" "Decimeters" "Meters" "Kilometers" "Inches" "Feet" "Yards" "Miles"  ) # 
# PATH: Import|AdvOptGrp|AxisConvGrp|AxisConversion    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Import|AdvOptGrp|AxisConvGrp|UpAxis    ( TYPE: Enum )  ( VALUE: "Y" )  (POSSIBLE VALUES: "Y" "Z"  ) # 
# PATH: Import|AdvOptGrp|UI|ShowWarningsManager    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|UI|GenerateLogData    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Obj|ReferenceNode    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Max_3ds|ReferenceNode    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Max_3ds|Texture    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Max_3ds|Material    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Max_3ds|Animation    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Max_3ds|Mesh    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Max_3ds|Light    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Max_3ds|Camera    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Max_3ds|AmbientLight    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Max_3ds|Rescaling    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Max_3ds|Filter    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Max_3ds|Smoothgroup    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Motion_Base|MotionFrameCount    ( TYPE: Integer ) ( VALUE: 0 ) # 
# PATH: Import|AdvOptGrp|FileFormat|Motion_Base|MotionFrameRate    ( TYPE: Number ) ( VALUE: 0.000000 ) # 
# PATH: Import|AdvOptGrp|FileFormat|Motion_Base|MotionActorPrefix    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Motion_Base|MotionRenameDuplicateNames    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Motion_Base|MotionExactZeroAsOccluded    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Motion_Base|MotionSetOccludedToLastValidPos    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Motion_Base|MotionAsOpticalSegments    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Motion_Base|MotionASFSceneOwned    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Motion_Base|MotionUpAxisUsedInFile    ( TYPE: Integer ) ( VALUE: 3 ) # 
# PATH: Import|AdvOptGrp|FileFormat|Biovision_BVH|MotionCreateReferenceNode    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|MotionAnalysis_HTR|MotionCreateReferenceNode    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|MotionAnalysis_HTR|MotionBaseTInOffset    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|MotionAnalysis_HTR|MotionBaseRInPrerotation    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionCreateReferenceNode    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionDummyNodes    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionLimits    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionBaseTInOffset    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionBaseRInPrerotation    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionCreateReferenceNode    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionDummyNodes    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionLimits    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionBaseTInOffset    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionBaseRInPrerotation    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|Dxf|WeldVertices    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|Dxf|ObjectDerivation    ( TYPE: Enum )  ( VALUE: "By layer" )  (POSSIBLE VALUES: "By layer" "By entity" "By block"  ) # 
# PATH: Import|AdvOptGrp|Dxf|ReferenceNode    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Import|AdvOptGrp|Performance|RemoveBadPolysFromMesh    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|PlugInGrp|PlugInUIWidth    ( TYPE: Integer ) ( VALUE: 500 ) # 
# PATH: Export|PlugInGrp|PlugInUIHeight    ( TYPE: Integer ) ( VALUE: 500 ) # 
# PATH: Export|PlugInGrp|PlugInUIXpos    ( TYPE: Integer ) ( VALUE: 100 ) # 
# PATH: Export|PlugInGrp|PlugInUIYpos    ( TYPE: Integer ) ( VALUE: 100 ) # 
# PATH: Export|PlugInGrp|UILIndex    ( TYPE: Enum )  ( VALUE: "ENU" )  (POSSIBLE VALUES: "ENU" "DEU" "FRA" "JPN" "KOR" "CHS" "PTB"  ) # 
# PATH: Export|IncludeGrp|Geometry|SmoothingGroups    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|IncludeGrp|Geometry|expHardEdges    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Geometry|TangentsandBinormals    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Geometry|SmoothMesh    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|IncludeGrp|Geometry|SelectionSet    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Geometry|BlindData    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|IncludeGrp|Geometry|AnimationOnly    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Geometry|Instances    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Geometry|ContainerObjects    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|IncludeGrp|Geometry|Triangulate    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Geometry|GeometryNurbsSurfaceAs    ( TYPE: Enum )  ( VALUE: "NURBS" )  (POSSIBLE VALUES: "NURBS" "Interactive Display Mesh" "Software Render Mesh"  ) # 
# PATH: Export|IncludeGrp|Animation    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Animation|ExtraGrp|UseSceneName    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Animation|ExtraGrp|RemoveSingleKey    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Animation|ExtraGrp|Quaternion    ( TYPE: Enum )  ( VALUE: "Resample As Euler Interpolation" )  (POSSIBLE VALUES: "Retain Quaternion Interpolation" "Set As Euler Interpolation" "Resample As Euler Interpolation"  ) # 
# PATH: Export|IncludeGrp|Animation|BakeComplexAnimation    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameStart    ( TYPE: Integer ) ( VALUE: 1 ) # 
# PATH: Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameEnd    ( TYPE: Integer ) ( VALUE: 200 ) # 
# PATH: Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameStep    ( TYPE: Integer ) ( VALUE: 1 ) # 
# PATH: Export|IncludeGrp|Animation|BakeComplexAnimation|ResampleAnimationCurves    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Animation|BakeComplexAnimation|HideComplexAnimationBakedWarning    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Animation|Deformation    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|IncludeGrp|Animation|Deformation|Skins    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|IncludeGrp|Animation|Deformation|Shape    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|IncludeGrp|Animation|Deformation|ShapeAttributes    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Animation|Deformation|ShapeAttributes|ShapeAttributesValues    ( TYPE: Enum )  ( VALUE: "Relative" )  (POSSIBLE VALUES: "Relative" "Absolute"  ) # 
# PATH: Export|IncludeGrp|Animation|CurveFilter    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedTPrec    ( TYPE: Number ) ( VALUE: 0.000100 ) # 
# PATH: Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedRPrec    ( TYPE: Number ) ( VALUE: 0.009000 ) # 
# PATH: Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedSPrec    ( TYPE: Number ) ( VALUE: 0.004000 ) # 
# PATH: Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedOPrec    ( TYPE: Number ) ( VALUE: 0.009000 ) # 
# PATH: Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|AutoTangentsOnly    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|IncludeGrp|Animation|PointCache    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Animation|PointCache|SelectionSetNameAsPointCache    ( TYPE: Enum )  ( VALUE: " " )  (POSSIBLE VALUES: " " "defaultLightSet" "defaultObjectSet"  ) # 
# PATH: Export|IncludeGrp|Animation|ConstraintsGrp|Constraint    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Animation|ConstraintsGrp|Character    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|CameraGrp|Camera    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|LightGrp|Light    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|Audio    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|EmbedTextureGrp|EmbedTexture    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|BindPose    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|IncludeGrp|PivotToNulls    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|BypassRrsInheritance    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|IncludeGrp|InputConnectionsGrp|IncludeChildren    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|IncludeGrp|InputConnectionsGrp|InputConnections    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|UnitsGrp|DynamicScaleConversion    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|UnitsGrp|UnitsSelector    ( TYPE: Enum )  ( VALUE: "Centimeters" )  (POSSIBLE VALUES: "Millimeters" "Centimeters" "Decimeters" "Meters" "Kilometers" "Inches" "Feet" "Yards" "Miles"  ) # 
# PATH: Export|AdvOptGrp|AxisConvGrp|UpAxis    ( TYPE: Enum )  ( VALUE: "Y" )  (POSSIBLE VALUES: "Y" "Z"  ) # 
# PATH: Export|AdvOptGrp|UI|ShowWarningsManager    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|UI|GenerateLogData    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Obj|Triangulate    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Obj|Deformation    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Motion_Base|MotionFrameCount    ( TYPE: Integer ) ( VALUE: 0 ) # 
# PATH: Export|AdvOptGrp|FileFormat|Motion_Base|MotionFromGlobalPosition    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Motion_Base|MotionFrameRate    ( TYPE: Number ) ( VALUE: 30.000000 ) # 
# PATH: Export|AdvOptGrp|FileFormat|Motion_Base|MotionGapsAsValidData    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Motion_Base|MotionC3DRealFormat    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Motion_Base|MotionASFSceneOwned    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Biovision_BVH|MotionTranslation    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionTranslation    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionFrameRateUsed    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionFrameRange    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionWriteDefaultAsBaseTR    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionTranslation    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionFrameRateUsed    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionFrameRange    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionWriteDefaultAsBaseTR    ( TYPE: Bool ) ( VALUE: "false" ) # 
# PATH: Export|AdvOptGrp|Fbx|AsciiFbx    ( TYPE: Enum )  ( VALUE: "Binary" )  (POSSIBLE VALUES: "Binary" "ASCII"  ) # 
# PATH: Export|AdvOptGrp|Fbx|ExportFileVersion    ( TYPE: Alias )  ( VALUE: "FBX202000" )  (POSSIBLE VALUES: "FBX202000" "FBX201900" "FBX201800" "FBX201600" "FBX201400" "FBX201300" "FBX201200" "FBX201100" "FBX201000" "FBX200900" "FBX200611"  ) # 
# PATH: Export|AdvOptGrp|Dxf|Deformation    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|Dxf|Triangulate    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|Collada|Triangulate    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|Collada|SingleMatrix    ( TYPE: Bool ) ( VALUE: "true" ) # 
# PATH: Export|AdvOptGrp|Collada|FrameRate    ( TYPE: Number ) ( VALUE: 24.000000 ) # 
"""


def convert_fbx_properties(properties):
    """
    Helper function to convert FBX properties returned by the `cmds.FBXProperties()` command
    into usable cmds commands.

    :param str properties: All of the FBX properties to convert
    :returns: List of string commands that can be used by Maya
    :rtype: str
    """
    standard_fbx_regex = r'^(# PATH: )(.*)    (\( TYPE: (\w+) \)) +(\( VALUE: (.+) \)) #'
    enum_fbx_regex = r'^(# PATH: )(.*)    (\( TYPE: (\w+) \)) .(\( VALUE: (.+) \)) +(\(POSSIBLE VALUES: (.+)  \)) #'

    result_commands = []
    for line in properties.split('\n'):
        regex_str = enum_fbx_regex if 'POSSIBLE VALUES' in line else standard_fbx_regex
        match = re.match(regex_str, line.strip())

        if match:
            data_type = match.group(4)
            raw_value = match.group(6)
            fbx_setting = match.group(2)

            if data_type == 'Integer':
                value = int(raw_value)
            elif data_type == 'Bool':
                value = 1 if 'true' in raw_value else 0
            elif data_type == 'Number':
                value = float(raw_value)
            elif data_type in ['Enum', 'Alias']:
                value = raw_value.replace('"', "'")
            else:
                # Unsupported data type
                continue

            result_commands.append("cmds.FBXProperty('{}', '-v', {})".format(fbx_setting, value))

    return result_commands


if __name__ == '__main__':
    [print(x) for x in convert_fbx_properties(fbx_properties)]

'''

cmds.FBXProperty('Import|PlugInGrp|PlugInUIWidth', '-v', 500)
cmds.FBXProperty('Import|PlugInGrp|PlugInUIHeight', '-v', 500)
cmds.FBXProperty('Import|PlugInGrp|PlugInUIXpos', '-v', 100)
cmds.FBXProperty('Import|PlugInGrp|PlugInUIYpos', '-v', 100)
cmds.FBXProperty('Import|PlugInGrp|UILIndex', '-v', 'ENU')
cmds.FBXProperty('Import|IncludeGrp|MergeMode', '-v', 'Add and update animation')
cmds.FBXProperty('Import|IncludeGrp|Geometry|UnlockNormals', '-v', 0)
cmds.FBXProperty('Import|IncludeGrp|Geometry|HardEdges', '-v', 0)
cmds.FBXProperty('Import|IncludeGrp|Geometry|BlindData', '-v', 1)
cmds.FBXProperty('Import|IncludeGrp|Animation', '-v', 1)
cmds.FBXProperty('Import|IncludeGrp|Animation|ExtraGrp|Take', '-v', 'No Animation')
cmds.FBXProperty('Import|IncludeGrp|Animation|ExtraGrp|TimeLine', '-v', 0)
cmds.FBXProperty('Import|IncludeGrp|Animation|ExtraGrp|BakeAnimationLayers', '-v', 1)
cmds.FBXProperty('Import|IncludeGrp|Animation|ExtraGrp|Markers', '-v', 0)
cmds.FBXProperty('Import|IncludeGrp|Animation|ExtraGrp|Quaternion', '-v', 'Resample As Euler Interpolation')
cmds.FBXProperty('Import|IncludeGrp|Animation|ExtraGrp|ProtectDrivenKeys', '-v', 0)
cmds.FBXProperty('Import|IncludeGrp|Animation|ExtraGrp|DeformNullsAsJoints', '-v', 1)
cmds.FBXProperty('Import|IncludeGrp|Animation|ExtraGrp|NullsToPivot', '-v', 1)
cmds.FBXProperty('Import|IncludeGrp|Animation|ExtraGrp|PointCache', '-v', 1)
cmds.FBXProperty('Import|IncludeGrp|Animation|Deformation', '-v', 1)
cmds.FBXProperty('Import|IncludeGrp|Animation|Deformation|Skins', '-v', 1)
cmds.FBXProperty('Import|IncludeGrp|Animation|Deformation|Shape', '-v', 1)
cmds.FBXProperty('Import|IncludeGrp|Animation|Deformation|ForceWeightNormalize', '-v', 0)
cmds.FBXProperty('Import|IncludeGrp|Animation|SamplingPanel|SamplingRateSelector', '-v', 'Scene')
cmds.FBXProperty('Import|IncludeGrp|Animation|SamplingPanel|CurveFilterSamplingRate', '-v', 30.0)
cmds.FBXProperty('Import|IncludeGrp|Animation|CurveFilter', '-v', 0)
cmds.FBXProperty('Import|IncludeGrp|Animation|ConstraintsGrp|Constraint', '-v', 0)
cmds.FBXProperty('Import|IncludeGrp|Animation|ConstraintsGrp|CharacterType', '-v', 'HumanIK')
cmds.FBXProperty('Import|IncludeGrp|CameraGrp|Camera', '-v', 1)
cmds.FBXProperty('Import|IncludeGrp|LightGrp|Light', '-v', 1)
cmds.FBXProperty('Import|IncludeGrp|Audio', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|UnitsGrp|DynamicScaleConversion', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|UnitsGrp|UnitsSelector', '-v', 'Millimeters')
cmds.FBXProperty('Import|AdvOptGrp|AxisConvGrp|AxisConversion', '-v', 0)
cmds.FBXProperty('Import|AdvOptGrp|AxisConvGrp|UpAxis', '-v', 'Y')
cmds.FBXProperty('Import|AdvOptGrp|UI|ShowWarningsManager', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|UI|GenerateLogData', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Obj|ReferenceNode', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Max_3ds|ReferenceNode', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Max_3ds|Texture', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Max_3ds|Material', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Max_3ds|Animation', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Max_3ds|Mesh', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Max_3ds|Light', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Max_3ds|Camera', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Max_3ds|AmbientLight', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Max_3ds|Rescaling', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Max_3ds|Filter', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Max_3ds|Smoothgroup', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Motion_Base|MotionFrameCount', '-v', 0)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Motion_Base|MotionFrameRate', '-v', 0.0)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Motion_Base|MotionActorPrefix', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Motion_Base|MotionRenameDuplicateNames', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Motion_Base|MotionExactZeroAsOccluded', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Motion_Base|MotionSetOccludedToLastValidPos', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Motion_Base|MotionAsOpticalSegments', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Motion_Base|MotionASFSceneOwned', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Motion_Base|MotionUpAxisUsedInFile', '-v', 3)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Biovision_BVH|MotionCreateReferenceNode', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|MotionAnalysis_HTR|MotionCreateReferenceNode', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|MotionAnalysis_HTR|MotionBaseTInOffset', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|MotionAnalysis_HTR|MotionBaseRInPrerotation', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionCreateReferenceNode', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionDummyNodes', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionLimits', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionBaseTInOffset', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionBaseRInPrerotation', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionCreateReferenceNode', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionDummyNodes', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionLimits', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionBaseTInOffset', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionBaseRInPrerotation', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|Dxf|WeldVertices', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|Dxf|ObjectDerivation', '-v', 'By layer')
cmds.FBXProperty('Import|AdvOptGrp|Dxf|ReferenceNode', '-v', 1)
cmds.FBXProperty('Import|AdvOptGrp|Performance|RemoveBadPolysFromMesh', '-v', 1)
cmds.FBXProperty('Export|PlugInGrp|PlugInUIWidth', '-v', 500)
cmds.FBXProperty('Export|PlugInGrp|PlugInUIHeight', '-v', 500)
cmds.FBXProperty('Export|PlugInGrp|PlugInUIXpos', '-v', 100)
cmds.FBXProperty('Export|PlugInGrp|PlugInUIYpos', '-v', 100)
cmds.FBXProperty('Export|PlugInGrp|UILIndex', '-v', 'ENU')
cmds.FBXProperty('Export|IncludeGrp|Geometry|SmoothingGroups', '-v', 1)
cmds.FBXProperty('Export|IncludeGrp|Geometry|expHardEdges', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Geometry|TangentsandBinormals', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Geometry|SmoothMesh', '-v', 1)
cmds.FBXProperty('Export|IncludeGrp|Geometry|SelectionSet', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Geometry|BlindData', '-v', 1)
cmds.FBXProperty('Export|IncludeGrp|Geometry|AnimationOnly', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Geometry|Instances', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Geometry|ContainerObjects', '-v', 1)
cmds.FBXProperty('Export|IncludeGrp|Geometry|Triangulate', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Geometry|GeometryNurbsSurfaceAs', '-v', 'NURBS')
cmds.FBXProperty('Export|IncludeGrp|Animation', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Animation|ExtraGrp|UseSceneName', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Animation|ExtraGrp|RemoveSingleKey', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Animation|ExtraGrp|Quaternion', '-v', 'Resample As Euler Interpolation')
cmds.FBXProperty('Export|IncludeGrp|Animation|BakeComplexAnimation', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameStart', '-v', 1)
cmds.FBXProperty('Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameEnd', '-v', 200)
cmds.FBXProperty('Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameStep', '-v', 1)
cmds.FBXProperty('Export|IncludeGrp|Animation|BakeComplexAnimation|ResampleAnimationCurves', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Animation|BakeComplexAnimation|HideComplexAnimationBakedWarning', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Animation|Deformation', '-v', 1)
cmds.FBXProperty('Export|IncludeGrp|Animation|Deformation|Skins', '-v', 1)
cmds.FBXProperty('Export|IncludeGrp|Animation|Deformation|Shape', '-v', 1)
cmds.FBXProperty('Export|IncludeGrp|Animation|Deformation|ShapeAttributes', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Animation|Deformation|ShapeAttributes|ShapeAttributesValues', '-v', 'Relative')
cmds.FBXProperty('Export|IncludeGrp|Animation|CurveFilter', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedTPrec', '-v', 0.0001)
cmds.FBXProperty('Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedRPrec', '-v', 0.009)
cmds.FBXProperty('Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedSPrec', '-v', 0.004)
cmds.FBXProperty('Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedOPrec', '-v', 0.009)
cmds.FBXProperty('Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|AutoTangentsOnly', '-v', 1)
cmds.FBXProperty('Export|IncludeGrp|Animation|PointCache', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Animation|PointCache|SelectionSetNameAsPointCache', '-v', ' ')
cmds.FBXProperty('Export|IncludeGrp|Animation|ConstraintsGrp|Constraint', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Animation|ConstraintsGrp|Character', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|CameraGrp|Camera', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|LightGrp|Light', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|Audio', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|EmbedTextureGrp|EmbedTexture', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|BindPose', '-v', 1)
cmds.FBXProperty('Export|IncludeGrp|PivotToNulls', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|BypassRrsInheritance', '-v', 0)
cmds.FBXProperty('Export|IncludeGrp|InputConnectionsGrp|IncludeChildren', '-v', 1)
cmds.FBXProperty('Export|IncludeGrp|InputConnectionsGrp|InputConnections', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|UnitsGrp|DynamicScaleConversion', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|UnitsGrp|UnitsSelector', '-v', 'Centimeters')
cmds.FBXProperty('Export|AdvOptGrp|AxisConvGrp|UpAxis', '-v', 'Y')
cmds.FBXProperty('Export|AdvOptGrp|UI|ShowWarningsManager', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|UI|GenerateLogData', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Obj|Triangulate', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Obj|Deformation', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Motion_Base|MotionFrameCount', '-v', 0)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Motion_Base|MotionFromGlobalPosition', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Motion_Base|MotionFrameRate', '-v', 30.0)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Motion_Base|MotionGapsAsValidData', '-v', 0)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Motion_Base|MotionC3DRealFormat', '-v', 0)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Motion_Base|MotionASFSceneOwned', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Biovision_BVH|MotionTranslation', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionTranslation', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionFrameRateUsed', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionFrameRange', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionWriteDefaultAsBaseTR', '-v', 0)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionTranslation', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionFrameRateUsed', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionFrameRange', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionWriteDefaultAsBaseTR', '-v', 0)
cmds.FBXProperty('Export|AdvOptGrp|Fbx|AsciiFbx', '-v', 'Binary')
cmds.FBXProperty('Export|AdvOptGrp|Fbx|ExportFileVersion', '-v', 'FBX202000')
cmds.FBXProperty('Export|AdvOptGrp|Dxf|Deformation', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|Dxf|Triangulate', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|Collada|Triangulate', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|Collada|SingleMatrix', '-v', 1)
cmds.FBXProperty('Export|AdvOptGrp|Collada|FrameRate', '-v', 24.0)

'''
