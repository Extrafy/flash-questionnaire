import service from '../../http/request';

export function getQ(data) {
    return service({
        url: '/api/qs/info/get_square_survey_data',
        method: 'post',
        data,
    });
}

export function collectQ(data) {
    return service({
        url: '/api/qs/Status/collect_survey',
        method: 'post',
        data,
    });
}

export function uncollectQ(data) {
    return service({
        url: '/api/qs/Status/cancel_collections',
        method: 'post',
        data,
    });
}

export function purchaseQ(data) {
    return service({
        url: '/api/qs/Status/buy_survey',
        method: 'post',
        data,
    });
}

export function getHistoryQ(data) {
    return service({
        url: '/api/qs/info/get_history',
        method: 'post',
        data,
    });
}