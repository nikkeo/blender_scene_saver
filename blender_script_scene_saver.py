import bpy
import requests
import getpass
from bpy.types import Operator, Panel
from datetime import datetime


API_URL = "http://localhost:8000/save_scene/"

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class SaveOperator(Operator):
    bl_idname = "object.save_operator"
    bl_label = "Save Scene"

    def execute(self, context):
        bpy.ops.wm.save_mainfile()
        self.report({'INFO'}, "Scene saved successfully!")

        user_name = getpass.getuser() or "Unknown User"
        save_time = datetime.now().isoformat()
        file_path = bpy.data.filepath

        data = {
            "username": user_name,
            "save_time": save_time,
            "file_path": file_path
        }

        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                self.report({'INFO'}, "Data sent to server successfully!")
            else:
                self.report({'WARNING'}, f"Failed to send data. Status: {response.status_code}")
        except Exception as e:
            self.report({'ERROR'}, f"Error sending data: {e}")


        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_idname = "OBJECT_PT_custom_panel"
    bl_label = "My Panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_context = "objectmode"   

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout

        layout.label(text="Save Scene:")
        layout.operator(SaveOperator.bl_idname, text="Save Scene", icon="FILE_TICK")
        layout.separator()

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_class(OBJECT_PT_CustomPanel)
    bpy.utils.register_class(SaveOperator)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_CustomPanel)
    bpy.utils.unregister_class(SaveOperator)

if __name__ == "__main__":
    register()
