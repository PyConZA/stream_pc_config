import json

import obspython as S

LAST_SCENE = ""

# Default scene names, in case you need to duplite your setup on multiple machines.
DEFAULT_SCENES = [
]
DEFAULT_PROJECTION_SCENES = [
]


def _from_data_t(data_t):
    j = S.obs_data_get_json(data_t)
    d = json.loads(j)
    return d["value"]

def _to_data_t(value):
    dic = {"hidden":False, "selected":False, "value":value}
    j = json.dumps(dic)
    return S.obs_data_create_from_json(j)

def _array_t_to_list(array_t):
    length = S.obs_data_array_count(array_t)
    data_t_list = [S.obs_data_array_item(array_t, i) for i in range(length)]
    return [_from_data_t(data_t) for data_t in data_t_list]

def _list_to_array_t(values):
    data_t_list = [_to_data_t(value) for value in values]
    array_t = S.obs_data_array_create()
    for data_t in data_t_list:
        S.obs_data_array_push_back(array_t, data_t)
    return array_t

def script_description():
    return (
        "Automatically project the scene that the current scene is mapped with in the "
        "properties.\n"
        "\n"
        "The two lists, `Scenes` and `Mapped projection scenes`, are mapped to one another, "
        "which means that for example, the first scene in the first list, maps to the "
        "first scene in the second list."
    )

def script_properties():
    properties = S.obs_properties_create()
    S.obs_properties_add_int(properties, "monitor", "Monitor to project to.", 0, 9, 1)
    S.obs_properties_add_editable_list(properties, "scenes", "Scenes", S.OBS_EDITABLE_LIST_TYPE_STRINGS, "", "")
    S.obs_properties_add_editable_list(properties, "projection_scenes", "Mapped projection scenes", S.OBS_EDITABLE_LIST_TYPE_STRINGS, "", "")
    return properties

def script_defaults(settings):
    S.obs_data_set_default_int(settings, "monitor", 1)
    for setting, default_values in (("scenes", DEFAULT_SCENES), ("projection_scenes", DEFAULT_PROJECTION_SCENES)):
        array_t = _list_to_array_t(default_values)
        S.obs_data_set_default_array(settings, setting, array_t)

def script_update(settings):
    global MONITOR
    MONITOR = S.obs_data_get_int(settings, "monitor")
    scenes_array_t = S.obs_data_get_array(settings, "scenes")
    global SCENES
    SCENES = _array_t_to_list(scenes_array_t)
    projection_scenes_array_t = S.obs_data_get_array(settings, "projection_scenes")
    global PROJECTION_SCENES
    PROJECTION_SCENES = _array_t_to_list(projection_scenes_array_t)

def on_change(event):
    if event != S.OBS_FRONTEND_EVENT_SCENE_CHANGED:
        return
    # We are making the dictionary here, as if its done in `script_update`, we will get
    # an exception each time an item is changed in the properties.
    mapping = dict(zip(SCENES, PROJECTION_SCENES))
    scene = S.obs_frontend_get_current_scene()
    scene_name = S.obs_source_get_name(scene)

    try:
        project_scene = mapping[scene_name]
    except KeyError:
        return

    global LAST_SCENE
    if project_scene != LAST_SCENE:
        S.obs_frontend_open_projector("Scene", MONITOR, "", project_scene)
    LAST_SCENE = project_scene

def script_load(settings):
    S.obs_frontend_add_event_callback(on_change)
