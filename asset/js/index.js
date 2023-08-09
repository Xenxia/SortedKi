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
        

        switch (selectedValue) {
            case "100to200": {
                const config = jsyaml.load(text)
                const newConfig = _100to200(config)
                saveYML(newConfig, file)
                break;
            }

            case "200to300":{
                const config = jsyaml.load(text)
                newConfig = _200to300(config)
                saveJSON(newConfig, file)
                break;
            }

            default:
                break;
        }

    } catch (e) {
        console.log(e);
    }

})

/**
 * 
 * @param {object} config
 * @param {File} file
 */
function saveYML(config, file) {
    const yml = jsyaml.dump(config, {
        "indent": 4,
        "noRefs": true,
        "condenseFlow": true

    })

    console.log(yml);

    saveAndDownload(yml, file);
}

/**
 * 
 * @param {object} config
 * @param {File} file
 */
function saveJSON(config, file) {
    const json = JSON.stringify(config)

    console.log(json);

    saveAndDownload(json, file.name.replace(".configTree.yml", ".confki.json"));
}

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

/**
 * 
 * @param {object} config
 * @returns {object}
 */
function _200to300(config) {

    const j = {};

    if (config["version_config_file"] != "2.0") {
        console.log("is not 2.0 version file")
        return j
    }

    j["config_sort"] = config["config_sort"]
    j["version_config_file"] = "3.0";
    j["sources"] = {
        "Root": {
            "path": ".",
            "disable": false
        }
    };
    j["unsorted"] = config["unsorted"] ?? false;
    j["sorting_exception"] = config["doNotSort"] ?? [];
    j["lang"] = config["lang"] ?? null;

    return j

}

/**
 * 
 * @param {object} content
 * @param {string} fileName
 * @returns {}
 */
function saveAndDownload(content, fileName) {
    const link = document.querySelector("a")

    let formBlob = new Blob([content], { type: 'text/plain' });

    link.href = window.URL.createObjectURL(formBlob);
    link.text = `⤓ Download : ${fileName}`
    link.download = `${fileName}`
}

// document.getElementById("Test").addEventListener("click", (event) => {
//     console.log("test");
//     saveAndDownload("test", "oui")
// })



