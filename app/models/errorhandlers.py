def register_handlers(app):
    from flask import render_template

    @app.errorhandler(400)
    def http400(error):
        return render_template('error/http400.html', message=error.description), 400

    @app.errorhandler(401)
    def http401(error):
        return render_template('error/http401.html'), 401

    @app.errorhandler(403)
    def http403(error):
        return render_template('error/http403.html'), 403

    @app.errorhandler(404)
    def http404(error):
        return render_template('error/http404.html'), 404

    @app.errorhandler(410)
    def http410(error):
        return render_template('error/http410.html'), 410

    @app.errorhandler(500)
    def http500(error):
        app.logger.error(error)
        return render_template('error/http500.html'), 500

    @app.errorhandler(503)
    def http503(error):
        return render_template('error/http503.html'), 503
