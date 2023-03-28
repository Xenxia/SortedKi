const input = document.querySelector("input");
const select = document.querySelector("select");

document.querySelector("form").addEventListener("submit", async (event) => {

    event.preventDefault();
    const file = input.files[0];
    const selectedValue = select.value;

    if (!file) {
        return
    }
    const text = await file.text();
    let newConfig = {}

    try {
        const config = jsyaml.load(text)

        switch (selectedValue) {
            case "100to200":
                newConfig = _100to200(config)
                break;

            default:
                break;
        }

    } catch (e) {
        console.log(e);
    }

    console.log(newConfig);
})


/**
 * 
 * @param {object} config
 * @returns {object}
 */
function _100to200(config) {

    const j = {};

    if (config["version_config_file"] == "2.0") {
        console.log("is 2.0 version file")
        return j
    }

    j["config_sort"] = {}
    j["version_config_file"] = "2.0";
    j["search_folder"] = [];
    j["unsorted"] = config["unsorted"] ?? false;
    j["doNotSort"] = config["doNotSort"] ?? [];
    j["lang"] = config["lang"] ?? null;

    for (let key in config["config_sort"]) {

        j["config_sort"][key] = {
            "disable": false,
            "parent": config["config_sort"][key].parent ?? null,
            "folder": config["config_sort"][key].folder,
            "fullPath": config["config_sort"][key].fullPath,
            "rule": config["config_sort"][key].ext ?? null,
            "pathStatic": false,
        }
    }

    return j

}



