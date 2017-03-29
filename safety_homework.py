from flask import Flask, render_template, url_for, jsonify, request, session
from flask_bootstrap import Bootstrap
from forms import stringForm
import hashlib, os
import rsa, base64

app = Flask(__name__)
app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = stringForm()
    md5String = ''
    if form.validate_on_submit():
        dataString = form.string.data
        md5String = hashlib.md5(dataString.encode()).hexdigest()
    return render_template('intro.html', form=form, md5String=md5String)


@app.route('/md5', methods=['GET', 'POST'])
def md5():
    form = stringForm()
    md5String = ''
    if form.validate_on_submit():
        dataString = form.string.data
        md5String = hashlib.md5(dataString.encode()).hexdigest()
    return render_template('md5.html', form=form, md5String=md5String)


@app.route('/RSA', methods=['GET', 'POST'])
def Rsa():
    form = stringForm()
    PubEncrypt = b''
    PubDecrypt = b''
    if form.validate_on_submit():
        dataString = form.string.data
        #with open('public.pem') as publickfile:
        #    p = publickfile.read()
        #    pubKey = rsa.PublicKey.load_pkcs1(p)
        #with open('private.pem') as privatefile:
        #    p = privatefile.read()
        #    prvKey = rsa.PrivateKey.load_pkcs1(p)
        pubKey, prvKey = rsa.PublicKey.load_pkcs1(session['key1']), rsa.PrivateKey.load_pkcs1(session['key2'])
        PubEncrypt = base64.b64encode(rsa.encrypt(dataString.encode('utf-8'), pubKey))
        PubDecrypt = rsa.decrypt(rsa.encrypt(dataString.encode('utf-8'), pubKey), prvKey)
        #print(PubDecrypt)
    return render_template('rsa.html', form=form, PubEncrypt=PubEncrypt.decode('utf-8'), PubDecrypt=PubDecrypt.decode('utf-8'))


@app.route('/api/KEYS')
def keys():
    (pubkey, privkey) = rsa.newkeys(512)
    #prifile = open('private.pem', 'w+')
    #prifile.write(privkey.save_pkcs1().decode('utf-8'))
    #prifile.close()
    #pubfile = open('public.pem', 'w+')
    #pubfile.write(pubkey.save_pkcs1().decode('utf-8'))
    #pubfile.close()
    session['key1'], session['key2'] = pubkey.save_pkcs1(), privkey.save_pkcs1()
    return jsonify({
        'key1': pubkey.save_pkcs1().decode('utf-8'),
        'key2': privkey.save_pkcs1().decode('utf-8')
    })


if __name__ == '__main__':
    app.run(debug=True)
