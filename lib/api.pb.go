// Code generated by protoc-gen-go. DO NOT EDIT.
// source: api.proto

package lib

import proto "github.com/golang/protobuf/proto"
import fmt "fmt"
import math "math"

import (
	context "golang.org/x/net/context"
	grpc "google.golang.org/grpc"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion2 // please upgrade the proto package

// The request message containing the user's name.
type FuzzyRequest struct {
	Qry                  string   `protobuf:"bytes,1,opt,name=qry" json:"qry,omitempty"`
	Cid                  string   `protobuf:"bytes,2,opt,name=cid" json:"cid,omitempty"`
	Algo                 string   `protobuf:"bytes,3,opt,name=algo" json:"algo,omitempty"`
	Max                  int32    `protobuf:"varint,4,opt,name=max" json:"max,omitempty"`
	Data                 []string `protobuf:"bytes,5,rep,name=data" json:"data,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *FuzzyRequest) Reset()         { *m = FuzzyRequest{} }
func (m *FuzzyRequest) String() string { return proto.CompactTextString(m) }
func (*FuzzyRequest) ProtoMessage()    {}
func (*FuzzyRequest) Descriptor() ([]byte, []int) {
	return fileDescriptor_api_0cfc304e8170fce1, []int{0}
}
func (m *FuzzyRequest) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_FuzzyRequest.Unmarshal(m, b)
}
func (m *FuzzyRequest) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_FuzzyRequest.Marshal(b, m, deterministic)
}
func (dst *FuzzyRequest) XXX_Merge(src proto.Message) {
	xxx_messageInfo_FuzzyRequest.Merge(dst, src)
}
func (m *FuzzyRequest) XXX_Size() int {
	return xxx_messageInfo_FuzzyRequest.Size(m)
}
func (m *FuzzyRequest) XXX_DiscardUnknown() {
	xxx_messageInfo_FuzzyRequest.DiscardUnknown(m)
}

var xxx_messageInfo_FuzzyRequest proto.InternalMessageInfo

func (m *FuzzyRequest) GetQry() string {
	if m != nil {
		return m.Qry
	}
	return ""
}

func (m *FuzzyRequest) GetCid() string {
	if m != nil {
		return m.Cid
	}
	return ""
}

func (m *FuzzyRequest) GetAlgo() string {
	if m != nil {
		return m.Algo
	}
	return ""
}

func (m *FuzzyRequest) GetMax() int32 {
	if m != nil {
		return m.Max
	}
	return 0
}

func (m *FuzzyRequest) GetData() []string {
	if m != nil {
		return m.Data
	}
	return nil
}

// The response message containing the greetings
type FuzzyReply struct {
	Code                 int32    `protobuf:"varint,1,opt,name=code" json:"code,omitempty"`
	Msg                  string   `protobuf:"bytes,2,opt,name=msg" json:"msg,omitempty"`
	Match                []string `protobuf:"bytes,3,rep,name=match" json:"match,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *FuzzyReply) Reset()         { *m = FuzzyReply{} }
func (m *FuzzyReply) String() string { return proto.CompactTextString(m) }
func (*FuzzyReply) ProtoMessage()    {}
func (*FuzzyReply) Descriptor() ([]byte, []int) {
	return fileDescriptor_api_0cfc304e8170fce1, []int{1}
}
func (m *FuzzyReply) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_FuzzyReply.Unmarshal(m, b)
}
func (m *FuzzyReply) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_FuzzyReply.Marshal(b, m, deterministic)
}
func (dst *FuzzyReply) XXX_Merge(src proto.Message) {
	xxx_messageInfo_FuzzyReply.Merge(dst, src)
}
func (m *FuzzyReply) XXX_Size() int {
	return xxx_messageInfo_FuzzyReply.Size(m)
}
func (m *FuzzyReply) XXX_DiscardUnknown() {
	xxx_messageInfo_FuzzyReply.DiscardUnknown(m)
}

var xxx_messageInfo_FuzzyReply proto.InternalMessageInfo

func (m *FuzzyReply) GetCode() int32 {
	if m != nil {
		return m.Code
	}
	return 0
}

func (m *FuzzyReply) GetMsg() string {
	if m != nil {
		return m.Msg
	}
	return ""
}

func (m *FuzzyReply) GetMatch() []string {
	if m != nil {
		return m.Match
	}
	return nil
}

type Empty struct {
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *Empty) Reset()         { *m = Empty{} }
func (m *Empty) String() string { return proto.CompactTextString(m) }
func (*Empty) ProtoMessage()    {}
func (*Empty) Descriptor() ([]byte, []int) {
	return fileDescriptor_api_0cfc304e8170fce1, []int{2}
}
func (m *Empty) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Empty.Unmarshal(m, b)
}
func (m *Empty) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Empty.Marshal(b, m, deterministic)
}
func (dst *Empty) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Empty.Merge(dst, src)
}
func (m *Empty) XXX_Size() int {
	return xxx_messageInfo_Empty.Size(m)
}
func (m *Empty) XXX_DiscardUnknown() {
	xxx_messageInfo_Empty.DiscardUnknown(m)
}

var xxx_messageInfo_Empty proto.InternalMessageInfo

type VersionReply struct {
	Sha                  string   `protobuf:"bytes,1,opt,name=sha" json:"sha,omitempty"`
	Branch               string   `protobuf:"bytes,2,opt,name=branch" json:"branch,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *VersionReply) Reset()         { *m = VersionReply{} }
func (m *VersionReply) String() string { return proto.CompactTextString(m) }
func (*VersionReply) ProtoMessage()    {}
func (*VersionReply) Descriptor() ([]byte, []int) {
	return fileDescriptor_api_0cfc304e8170fce1, []int{3}
}
func (m *VersionReply) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_VersionReply.Unmarshal(m, b)
}
func (m *VersionReply) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_VersionReply.Marshal(b, m, deterministic)
}
func (dst *VersionReply) XXX_Merge(src proto.Message) {
	xxx_messageInfo_VersionReply.Merge(dst, src)
}
func (m *VersionReply) XXX_Size() int {
	return xxx_messageInfo_VersionReply.Size(m)
}
func (m *VersionReply) XXX_DiscardUnknown() {
	xxx_messageInfo_VersionReply.DiscardUnknown(m)
}

var xxx_messageInfo_VersionReply proto.InternalMessageInfo

func (m *VersionReply) GetSha() string {
	if m != nil {
		return m.Sha
	}
	return ""
}

func (m *VersionReply) GetBranch() string {
	if m != nil {
		return m.Branch
	}
	return ""
}

func init() {
	proto.RegisterType((*FuzzyRequest)(nil), "lib.FuzzyRequest")
	proto.RegisterType((*FuzzyReply)(nil), "lib.FuzzyReply")
	proto.RegisterType((*Empty)(nil), "lib.Empty")
	proto.RegisterType((*VersionReply)(nil), "lib.VersionReply")
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConn

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion4

// FuzzyClient is the client API for Fuzzy service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type FuzzyClient interface {
	// Sends a greeting
	Match(ctx context.Context, in *FuzzyRequest, opts ...grpc.CallOption) (*FuzzyReply, error)
	Version(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*VersionReply, error)
}

type fuzzyClient struct {
	cc *grpc.ClientConn
}

func NewFuzzyClient(cc *grpc.ClientConn) FuzzyClient {
	return &fuzzyClient{cc}
}

func (c *fuzzyClient) Match(ctx context.Context, in *FuzzyRequest, opts ...grpc.CallOption) (*FuzzyReply, error) {
	out := new(FuzzyReply)
	err := c.cc.Invoke(ctx, "/lib.Fuzzy/Match", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *fuzzyClient) Version(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*VersionReply, error) {
	out := new(VersionReply)
	err := c.cc.Invoke(ctx, "/lib.Fuzzy/Version", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// Server API for Fuzzy service

type FuzzyServer interface {
	// Sends a greeting
	Match(context.Context, *FuzzyRequest) (*FuzzyReply, error)
	Version(context.Context, *Empty) (*VersionReply, error)
}

func RegisterFuzzyServer(s *grpc.Server, srv FuzzyServer) {
	s.RegisterService(&_Fuzzy_serviceDesc, srv)
}

func _Fuzzy_Match_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(FuzzyRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(FuzzyServer).Match(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/lib.Fuzzy/Match",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(FuzzyServer).Match(ctx, req.(*FuzzyRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Fuzzy_Version_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(FuzzyServer).Version(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/lib.Fuzzy/Version",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(FuzzyServer).Version(ctx, req.(*Empty))
	}
	return interceptor(ctx, in, info, handler)
}

var _Fuzzy_serviceDesc = grpc.ServiceDesc{
	ServiceName: "lib.Fuzzy",
	HandlerType: (*FuzzyServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "Match",
			Handler:    _Fuzzy_Match_Handler,
		},
		{
			MethodName: "Version",
			Handler:    _Fuzzy_Version_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "api.proto",
}

func init() { proto.RegisterFile("api.proto", fileDescriptor_api_0cfc304e8170fce1) }

var fileDescriptor_api_0cfc304e8170fce1 = []byte{
	// 258 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x4c, 0x50, 0xcd, 0x6a, 0xf3, 0x30,
	0x10, 0x8c, 0x3f, 0x45, 0x09, 0x59, 0x02, 0x5f, 0xba, 0x94, 0x22, 0x72, 0x32, 0x3a, 0x85, 0x42,
	0x7d, 0x68, 0x2f, 0x7d, 0x81, 0x96, 0x5e, 0x7a, 0xf1, 0xa1, 0x77, 0xf9, 0x07, 0x5b, 0x20, 0x47,
	0x8a, 0xa5, 0x40, 0x95, 0xa7, 0x2f, 0x5a, 0x3b, 0xe0, 0xdb, 0xec, 0x68, 0x34, 0x33, 0xbb, 0xb0,
	0x53, 0x4e, 0x17, 0x6e, 0xb4, 0xc1, 0x22, 0x33, 0xba, 0x92, 0x06, 0xf6, 0x9f, 0xd7, 0xdb, 0x2d,
	0x96, 0xed, 0xe5, 0xda, 0xfa, 0x80, 0x07, 0x60, 0x97, 0x31, 0x8a, 0x2c, 0xcf, 0x4e, 0xbb, 0x32,
	0xc1, 0xc4, 0xd4, 0xba, 0x11, 0xff, 0x26, 0xa6, 0xd6, 0x0d, 0x22, 0xac, 0x95, 0xe9, 0xac, 0x60,
	0x44, 0x11, 0x4e, 0xaa, 0x41, 0xfd, 0x8a, 0x75, 0x9e, 0x9d, 0x78, 0x99, 0x60, 0x52, 0x35, 0x2a,
	0x28, 0xc1, 0x73, 0x96, 0x54, 0x09, 0xcb, 0x2f, 0x80, 0x39, 0xcd, 0x99, 0x98, 0x14, 0xb5, 0x6d,
	0x5a, 0x0a, 0xe3, 0x25, 0x61, 0xf2, 0xf1, 0xdd, 0x3d, 0x6d, 0xf0, 0x1d, 0x3e, 0x02, 0x1f, 0x54,
	0xa8, 0x7b, 0xc1, 0xc8, 0x68, 0x1a, 0xe4, 0x16, 0xf8, 0xc7, 0xe0, 0x42, 0x94, 0xef, 0xb0, 0xff,
	0x69, 0x47, 0xaf, 0xed, 0x79, 0x32, 0x3d, 0x00, 0xf3, 0xbd, 0xba, 0x2f, 0xe0, 0x7b, 0x85, 0x4f,
	0xb0, 0xa9, 0x46, 0x75, 0xae, 0xfb, 0xd9, 0x75, 0x9e, 0x5e, 0x2b, 0xe0, 0x54, 0x06, 0x5f, 0x80,
	0x7f, 0x27, 0x53, 0x7c, 0x28, 0x8c, 0xae, 0x8a, 0xe5, 0x3d, 0x8e, 0xff, 0x97, 0x94, 0x33, 0x51,
	0xae, 0xf0, 0x19, 0xb6, 0x73, 0x22, 0x02, 0xbd, 0x52, 0x91, 0xe3, 0xf4, 0x79, 0xd9, 0x45, 0xae,
	0xaa, 0x0d, 0x9d, 0xfa, 0xed, 0x2f, 0x00, 0x00, 0xff, 0xff, 0xd7, 0x76, 0x82, 0x8f, 0x77, 0x01,
	0x00, 0x00,
}
