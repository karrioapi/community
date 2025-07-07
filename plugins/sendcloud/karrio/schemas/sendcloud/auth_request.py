import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ClientIDType:
    type: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class GrantTypeObjectType:
    type: typing.Optional[str] = None
    enum: typing.Optional[typing.List[str]] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PropertiesType:
    granttype: typing.Optional[GrantTypeObjectType] = jstruct.JStruct[GrantTypeObjectType]
    clientid: typing.Optional[ClientIDType] = jstruct.JStruct[ClientIDType]
    clientsecret: typing.Optional[ClientIDType] = jstruct.JStruct[ClientIDType]
    refreshtoken: typing.Optional[ClientIDType] = jstruct.JStruct[ClientIDType]
    scope: typing.Optional[ClientIDType] = jstruct.JStruct[ClientIDType]


@attr.s(auto_attribs=True)
class AuthRequestType:
    type: typing.Optional[str] = None
    properties: typing.Optional[PropertiesType] = jstruct.JStruct[PropertiesType]
    required: typing.Optional[typing.List[str]] = None
