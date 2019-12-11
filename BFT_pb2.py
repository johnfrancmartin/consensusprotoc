# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: BFT.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='BFT.proto',
  package='bft',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\tBFT.proto\x12\x03\x62\x66t\"\xd4\x01\n\x07Wrapper\x12\n\n\x02id\x18\x01 \x02(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x02\x12\x1b\n\x03\x62ls\x18\x03 \x01(\x0b\x32\x0e.bft.BLSHelper\x12\x1f\n\x08proposal\x18\x08 \x01(\x0b\x32\r.bft.Proposal\x12\x17\n\x04vote\x18\t \x01(\x0b\x32\t.bft.Vote\x12\x19\n\x05\x62lame\x18\n \x01(\x0b\x32\n.bft.Blame\x12\x1d\n\x07\x63ommand\x18\x0b \x01(\x0b\x32\x0c.bft.Command\x12\x19\n\x05\x65nter\x18\x0c \x01(\x0b\x32\n.bft.Enter\"\x81\x01\n\x05\x42lock\x12\x10\n\x08\x63ommands\x18\x01 \x03(\t\x12\x0f\n\x04view\x18\x02 \x01(\x05:\x01\x30\x12\x11\n\x06height\x18\x03 \x01(\x05:\x01\x30\x12\x11\n\tlock_cert\x18\x04 \x01(\t\x12\x10\n\x08previous\x18\x05 \x01(\t\x12\x0b\n\x03hqc\x18\x06 \x01(\x05\x12\x10\n\x08hotstuff\x18\x07 \x01(\x08\"\x1b\n\x07\x43ommand\x12\x10\n\x08\x63ommands\x18\x01 \x03(\t\"\xad\x01\n\tBLSHelper\x12\t\n\x01t\x18\x01 \x01(\x05\x12\t\n\x01n\x18\x02 \x01(\x05\x12\x10\n\x08sk_bytes\x18\x03 \x01(\x0c\x12\x10\n\x08g1_bytes\x18\x04 \x01(\x0c\x12\x10\n\x08g2_bytes\x18\x05 \x01(\x0c\x12\x15\n\roptimize_mult\x18\x06 \x01(\x08\x12\x11\n\tgroup_nid\x18\x07 \x01(\x05\x12\x14\n\x0csk_bytes_set\x18\x08 \x03(\x0c\x12\x14\n\x0cvk_bytes_set\x18\t \x03(\x0c\"H\n\tSignature\x12\x15\n\roptimize_mult\x18\x01 \x01(\x08\x12\x11\n\tgroup_nid\x18\x02 \x01(\x05\x12\x11\n\tsig_bytes\x18\x03 \x01(\x0c\"!\n\x0b\x43\x65rtificate\x12\x12\n\ncert_bytes\x18\x01 \x01(\x0c\"B\n\x03Key\x12\x15\n\roptimize_mult\x18\x01 \x01(\x08\x12\x11\n\tgroup_nid\x18\x02 \x01(\x05\x12\x11\n\tsig_bytes\x18\x03 \x01(\x0c\"5\n\x06Status\x12\x1a\n\x06locked\x18\x01 \x01(\x0b\x32\n.bft.Block\x12\x0f\n\x07replica\x18\x02 \x01(\x05\"a\n\x08Proposal\x12\x19\n\x05\x62lock\x18\x01 \x01(\x0b\x32\n.bft.Block\x12\x0c\n\x04view\x18\x02 \x01(\x05\x12\x10\n\x08previous\x18\x04 \x01(\t\x12\x1a\n\x06status\x18\x05 \x03(\x0b\x32\n.bft.Block\"R\n\x04Vote\x12\x19\n\x05\x62lock\x18\x01 \x01(\x0b\x32\n.bft.Block\x12\x0c\n\x04view\x18\x02 \x01(\x05\x12\x11\n\tsignature\x18\x03 \x01(\t\x12\x0e\n\x06sender\x18\x04 \x01(\x05\"B\n\x05\x42lame\x12\x0c\n\x04view\x18\x02 \x01(\x05\x12\x0e\n\x06sender\x18\x04 \x01(\x05\x12\x1b\n\x06states\x18\x05 \x03(\x0b\x32\x0b.bft.Status\"B\n\x05\x45nter\x12\x0c\n\x04view\x18\x02 \x01(\x05\x12\x0e\n\x06sender\x18\x04 \x01(\x05\x12\x1b\n\x06states\x18\x05 \x03(\x0b\x32\x0b.bft.Status')
)




_WRAPPER = _descriptor.Descriptor(
  name='Wrapper',
  full_name='bft.Wrapper',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='bft.Wrapper.id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='bft.Wrapper.timestamp', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bls', full_name='bft.Wrapper.bls', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='proposal', full_name='bft.Wrapper.proposal', index=3,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vote', full_name='bft.Wrapper.vote', index=4,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='blame', full_name='bft.Wrapper.blame', index=5,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='command', full_name='bft.Wrapper.command', index=6,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enter', full_name='bft.Wrapper.enter', index=7,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=231,
)


_BLOCK = _descriptor.Descriptor(
  name='Block',
  full_name='bft.Block',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='commands', full_name='bft.Block.commands', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='view', full_name='bft.Block.view', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='height', full_name='bft.Block.height', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lock_cert', full_name='bft.Block.lock_cert', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='previous', full_name='bft.Block.previous', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hqc', full_name='bft.Block.hqc', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hotstuff', full_name='bft.Block.hotstuff', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=234,
  serialized_end=363,
)


_COMMAND = _descriptor.Descriptor(
  name='Command',
  full_name='bft.Command',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='commands', full_name='bft.Command.commands', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=365,
  serialized_end=392,
)


_BLSHELPER = _descriptor.Descriptor(
  name='BLSHelper',
  full_name='bft.BLSHelper',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='t', full_name='bft.BLSHelper.t', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='n', full_name='bft.BLSHelper.n', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sk_bytes', full_name='bft.BLSHelper.sk_bytes', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='g1_bytes', full_name='bft.BLSHelper.g1_bytes', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='g2_bytes', full_name='bft.BLSHelper.g2_bytes', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='optimize_mult', full_name='bft.BLSHelper.optimize_mult', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='group_nid', full_name='bft.BLSHelper.group_nid', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sk_bytes_set', full_name='bft.BLSHelper.sk_bytes_set', index=7,
      number=8, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vk_bytes_set', full_name='bft.BLSHelper.vk_bytes_set', index=8,
      number=9, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=395,
  serialized_end=568,
)


_SIGNATURE = _descriptor.Descriptor(
  name='Signature',
  full_name='bft.Signature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='optimize_mult', full_name='bft.Signature.optimize_mult', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='group_nid', full_name='bft.Signature.group_nid', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sig_bytes', full_name='bft.Signature.sig_bytes', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=570,
  serialized_end=642,
)


_CERTIFICATE = _descriptor.Descriptor(
  name='Certificate',
  full_name='bft.Certificate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cert_bytes', full_name='bft.Certificate.cert_bytes', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=644,
  serialized_end=677,
)


_KEY = _descriptor.Descriptor(
  name='Key',
  full_name='bft.Key',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='optimize_mult', full_name='bft.Key.optimize_mult', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='group_nid', full_name='bft.Key.group_nid', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sig_bytes', full_name='bft.Key.sig_bytes', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=679,
  serialized_end=745,
)


_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='bft.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locked', full_name='bft.Status.locked', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='replica', full_name='bft.Status.replica', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=747,
  serialized_end=800,
)


_PROPOSAL = _descriptor.Descriptor(
  name='Proposal',
  full_name='bft.Proposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='block', full_name='bft.Proposal.block', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='view', full_name='bft.Proposal.view', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='previous', full_name='bft.Proposal.previous', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='bft.Proposal.status', index=3,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=802,
  serialized_end=899,
)


_VOTE = _descriptor.Descriptor(
  name='Vote',
  full_name='bft.Vote',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='block', full_name='bft.Vote.block', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='view', full_name='bft.Vote.view', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signature', full_name='bft.Vote.signature', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sender', full_name='bft.Vote.sender', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=901,
  serialized_end=983,
)


_BLAME = _descriptor.Descriptor(
  name='Blame',
  full_name='bft.Blame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='view', full_name='bft.Blame.view', index=0,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sender', full_name='bft.Blame.sender', index=1,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='states', full_name='bft.Blame.states', index=2,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=985,
  serialized_end=1051,
)


_ENTER = _descriptor.Descriptor(
  name='Enter',
  full_name='bft.Enter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='view', full_name='bft.Enter.view', index=0,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sender', full_name='bft.Enter.sender', index=1,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='states', full_name='bft.Enter.states', index=2,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1053,
  serialized_end=1119,
)

_WRAPPER.fields_by_name['bls'].message_type = _BLSHELPER
_WRAPPER.fields_by_name['proposal'].message_type = _PROPOSAL
_WRAPPER.fields_by_name['vote'].message_type = _VOTE
_WRAPPER.fields_by_name['blame'].message_type = _BLAME
_WRAPPER.fields_by_name['command'].message_type = _COMMAND
_WRAPPER.fields_by_name['enter'].message_type = _ENTER
_STATUS.fields_by_name['locked'].message_type = _BLOCK
_PROPOSAL.fields_by_name['block'].message_type = _BLOCK
_PROPOSAL.fields_by_name['status'].message_type = _BLOCK
_VOTE.fields_by_name['block'].message_type = _BLOCK
_BLAME.fields_by_name['states'].message_type = _STATUS
_ENTER.fields_by_name['states'].message_type = _STATUS
DESCRIPTOR.message_types_by_name['Wrapper'] = _WRAPPER
DESCRIPTOR.message_types_by_name['Block'] = _BLOCK
DESCRIPTOR.message_types_by_name['Command'] = _COMMAND
DESCRIPTOR.message_types_by_name['BLSHelper'] = _BLSHELPER
DESCRIPTOR.message_types_by_name['Signature'] = _SIGNATURE
DESCRIPTOR.message_types_by_name['Certificate'] = _CERTIFICATE
DESCRIPTOR.message_types_by_name['Key'] = _KEY
DESCRIPTOR.message_types_by_name['Status'] = _STATUS
DESCRIPTOR.message_types_by_name['Proposal'] = _PROPOSAL
DESCRIPTOR.message_types_by_name['Vote'] = _VOTE
DESCRIPTOR.message_types_by_name['Blame'] = _BLAME
DESCRIPTOR.message_types_by_name['Enter'] = _ENTER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Wrapper = _reflection.GeneratedProtocolMessageType('Wrapper', (_message.Message,), {
  'DESCRIPTOR' : _WRAPPER,
  '__module__' : 'BFT_pb2'
  # @@protoc_insertion_point(class_scope:bft.Wrapper)
  })
_sym_db.RegisterMessage(Wrapper)

Block = _reflection.GeneratedProtocolMessageType('Block', (_message.Message,), {
  'DESCRIPTOR' : _BLOCK,
  '__module__' : 'BFT_pb2'
  # @@protoc_insertion_point(class_scope:bft.Block)
  })
_sym_db.RegisterMessage(Block)

Command = _reflection.GeneratedProtocolMessageType('Command', (_message.Message,), {
  'DESCRIPTOR' : _COMMAND,
  '__module__' : 'BFT_pb2'
  # @@protoc_insertion_point(class_scope:bft.Command)
  })
_sym_db.RegisterMessage(Command)

BLSHelper = _reflection.GeneratedProtocolMessageType('BLSHelper', (_message.Message,), {
  'DESCRIPTOR' : _BLSHELPER,
  '__module__' : 'BFT_pb2'
  # @@protoc_insertion_point(class_scope:bft.BLSHelper)
  })
_sym_db.RegisterMessage(BLSHelper)

Signature = _reflection.GeneratedProtocolMessageType('Signature', (_message.Message,), {
  'DESCRIPTOR' : _SIGNATURE,
  '__module__' : 'BFT_pb2'
  # @@protoc_insertion_point(class_scope:bft.Signature)
  })
_sym_db.RegisterMessage(Signature)

Certificate = _reflection.GeneratedProtocolMessageType('Certificate', (_message.Message,), {
  'DESCRIPTOR' : _CERTIFICATE,
  '__module__' : 'BFT_pb2'
  # @@protoc_insertion_point(class_scope:bft.Certificate)
  })
_sym_db.RegisterMessage(Certificate)

Key = _reflection.GeneratedProtocolMessageType('Key', (_message.Message,), {
  'DESCRIPTOR' : _KEY,
  '__module__' : 'BFT_pb2'
  # @@protoc_insertion_point(class_scope:bft.Key)
  })
_sym_db.RegisterMessage(Key)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'BFT_pb2'
  # @@protoc_insertion_point(class_scope:bft.Status)
  })
_sym_db.RegisterMessage(Status)

Proposal = _reflection.GeneratedProtocolMessageType('Proposal', (_message.Message,), {
  'DESCRIPTOR' : _PROPOSAL,
  '__module__' : 'BFT_pb2'
  # @@protoc_insertion_point(class_scope:bft.Proposal)
  })
_sym_db.RegisterMessage(Proposal)

Vote = _reflection.GeneratedProtocolMessageType('Vote', (_message.Message,), {
  'DESCRIPTOR' : _VOTE,
  '__module__' : 'BFT_pb2'
  # @@protoc_insertion_point(class_scope:bft.Vote)
  })
_sym_db.RegisterMessage(Vote)

Blame = _reflection.GeneratedProtocolMessageType('Blame', (_message.Message,), {
  'DESCRIPTOR' : _BLAME,
  '__module__' : 'BFT_pb2'
  # @@protoc_insertion_point(class_scope:bft.Blame)
  })
_sym_db.RegisterMessage(Blame)

Enter = _reflection.GeneratedProtocolMessageType('Enter', (_message.Message,), {
  'DESCRIPTOR' : _ENTER,
  '__module__' : 'BFT_pb2'
  # @@protoc_insertion_point(class_scope:bft.Enter)
  })
_sym_db.RegisterMessage(Enter)


# @@protoc_insertion_point(module_scope)
