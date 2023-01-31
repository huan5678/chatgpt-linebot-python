def get_commands():
    return [
        {
            'chatGPT相關指令': [{
                '重新輸入': {
                    'type': 'message',
                    'text': '/redo',
                },
            }, {
                '清除紀錄': {
                    'type': 'message',
                    'text': '/clear',
                },
            }, {
                '設定token': {
                    'type': 'postback',
                    'text': '/token [數字]',
                },
            }, {
                '切換頻率': {
                    'type': 'postback',
                    'text': '/setFrequency [數字]',
                },
            }, {
                '切換模型': {
                    'type': 'postback',
                    'text': '/setModel [模型名稱]',
                },
            }, {
                '模型列表': {
                    'type': 'message',
                    'text': '/modelList',
                },
            }, {
                '狀態': {
                    'type': 'message',
                    'text': '/status',
                },
            }, {
                '查看歷史紀錄': {
                    'type': 'message',
                    'text': '/history',
                },
            }],
        },
        {
            '匯率': [
                {
                    '台幣匯率查詢': {
                        'type': 'message',
                        'text': '/匯率'
                    },
                },
            ],
        },
        {
            '隨機選取': [
                {
                    '從列表中隨機選擇': {
                        'type': 'message',
                        'text': '/隨選'
                    },
                },
            ],
        },
    ]
