from entrypoint import app,SETTINGS

if SETTINGS.MODE == 'server':
    app.run(host='0.0.0.0', port=8004, debug=True)
