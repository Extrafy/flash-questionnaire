import service from "../../http/request";

export function getQ(data) {
    return service({
        url: '/api/qs/info/get_survey_in_recyclebin_data',
        method: 'post',
        data,
    });
}

export function deleteQ(data) {
    return service({
        url: '/api/qs/Status/delete_survey_real',
        method: 'post',
        data,
    });
}
export function deleteAll(data) {
    return service({
        url: '/api/qs/Status/delete_all_survey_real',
        method: 'post',
        data,
    });
}
export function recycleQ(data) {
    return service({
        url: '/api/qs/Status/recover_survey_from_delete',
        method: 'post',
        data,
    });
}