import service from '../../http/request';

export function initialize(data) {
    return service({
        url: 'api/qs/ms-fill-analyse/data_analysis_FS',
        method: 'POST',
        data: data,
    });
}

export function getStatistic(data) {
    return service({
        url: 'api/qs/ms-fill-analyse/data_analysis_SE',
        method: 'POST',
        data: data,
    });
}

export function getData(data) {
    return service({
        url: 'api/qs/ms-fill-analyse/data_analysis_TH',
        method: 'POST',
        data: data,
    });
}