# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from app.database import Column, Model, SurrogatePK, db, reference_col, relationship, CRUDMixin
from app.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)


class RawData(Model, SurrogatePK, CRUDMixin):
    """AirSim RawData"""

    __tablename__ = "rawdatas"
    gear = Column(db.Integer, nullable=False)
    handbreak = Column(db.Boolean, nullable=False)
    maxrpm = Column(db.Float, nullable=False)
    rpm = Column(db.Float, nullable=False)
    speed = Column(db.Float, nullable=False)
    timestamp = Column(db.TIMESTAMP(True), nullable=False, server_default=db.text('NOW()'))
    pos_x = Column(db.Float, nullable=False)
    pos_y = Column(db.Float, nullable=False)
    pos_z = Column(db.Float, nullable=False)
    aa_x = Column(db.Float, nullable=False)
    aa_y = Column(db.Float, nullable=False)
    aa_z = Column(db.Float, nullable=False)
    av_x = Column(db.Float, nullable=False)
    av_y = Column(db.Float, nullable=False)
    av_z = Column(db.Float, nullable=False)
    la_x = Column(db.Float, nullable=False)
    la_y = Column(db.Float, nullable=False)
    la_z = Column(db.Float, nullable=False)
    lv_x = Column(db.Float, nullable=False)
    lv_y = Column(db.Float, nullable=False)
    lv_z = Column(db.Float, nullable=False)

    def __init__(self, gear, handbreak, maxrpm, rpm, speed, pos_x, pos_y, pos_z, aa_x, aa_y, aa_z, av_x,
                 av_y, av_z, la_x, la_y, la_z, lv_x, lv_y, lv_z):
        db.Model.__init__(self, gear=gear, handbreak=handbreak, maxrpm=maxrpm, rpm=rpm, speed=speed, pos_x=pos_x,
                          pos_y=pos_y, pos_z=pos_z, aa_x=aa_x, aa_y=aa_y, aa_z=aa_z,
                          av_x=av_x, av_y=av_y, av_z=av_z, la_x=la_x, la_y=la_y, la_z=la_z, lv_x=lv_x, lv_y=lv_y,
                          lv_z=lv_z)
