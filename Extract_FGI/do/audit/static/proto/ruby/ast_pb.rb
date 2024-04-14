# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ast.proto

require 'google/protobuf'

Google::Protobuf::DescriptorPool.generated_pool.build do
  add_message "proto.FileInfo" do
    optional :filename, :string, 1
    optional :relpath, :string, 2
    optional :file, :string, 3
    optional :directory, :string, 4
  end
  add_message "proto.SourceLocation" do
    optional :row, :int32, 1
    optional :column, :int32, 2
    optional :file_info, :message, 3, "proto.FileInfo"
  end
  add_message "proto.SourceRange" do
    optional :start, :message, 1, "proto.SourceLocation"
    optional :end, :message, 2, "proto.SourceLocation"
  end
  add_message "proto.AstNode" do
    optional :type, :enum, 1, "proto.AstNode.NodeType"
    optional :name, :string, 2
    optional :full_name, :string, 3
    optional :base_type, :string, 4
    optional :module, :string, 5
    optional :value, :string, 6
    optional :definition, :string, 7
    repeated :arg_nodes, :message, 8, "proto.AstNode"
    repeated :arguments, :string, 9
    optional :source, :string, 10
    optional :range, :message, 11, "proto.SourceRange"
    optional :id, :int32, 12
    optional :functionality, :enum, 13, "proto.Functionality"
    repeated :child_nodes, :message, 18, "proto.AstNode"
    optional :instantiatable, :bool, 19
    oneof :accurate_functionality do
      optional :source_type, :enum, 14, "proto.SourceType"
      optional :sink_type, :enum, 15, "proto.SinkType"
      optional :danger_type, :enum, 16, "proto.DangerType"
      optional :propagate_type, :enum, 17, "proto.PropagateType"
    end
  end
  add_enum "proto.AstNode.NodeType" do
    value :UNKNOWN, 0
    value :FUNCTION_DECL, 1
    value :VARIABLE_DECL, 2
    value :CLASS_DECL, 3
    value :FUNCTION_DECL_REF_EXPR, 11
    value :VARIABLE_DECL_REF_EXPR, 12
    value :CLASS_DECL_REF_EXPR, 13
    value :PY_FUNCTION_DEF, 101
    value :JS_ASSIGNMENT_EXPRESSION, 201
    value :RB_REGULAR_NODE, 301
    value :RB_VARIABLE_NODE, 302
    value :JAVA_IDENTITY_STMT, 401
    value :PHP_EXPR_VARIABLE, 501
  end
  add_message "proto.AstLookupConfig" do
    repeated :apis, :message, 1, "proto.AstNode"
    optional :save_feature, :bool, 2
    optional :smt_formula, :string, 3
    optional :smt_satisfied, :bool, 4
    optional :func_only, :bool, 5
  end
  add_message "proto.PkgAstResult" do
    optional :pkg_name, :string, 1
    optional :pkg_version, :string, 2
    optional :language, :enum, 3, "proto.Language"
    optional :input_path, :string, 4
    optional :config, :message, 5, "proto.AstLookupConfig"
    repeated :api_results, :message, 6, "proto.AstNode"
    repeated :root_nodes, :message, 7, "proto.AstNode"
  end
  add_message "proto.PkgAstResults" do
    repeated :pkgs, :message, 1, "proto.PkgAstResult"
    optional :timestamp, :uint64, 2
  end
  add_enum "proto.Language" do
    value :UNKNOWN, 0
    value :PYTHON, 1
    value :JAVASCRIPT, 2
    value :RUBY, 3
    value :JAVA, 4
    value :PHP, 5
    value :CSHARP, 6
    value :CPP, 7
    value :GO, 8
  end
  add_enum "proto.Functionality" do
    value :UNCLASSIFIED, 0
    value :SOURCE, 1
    value :SINK, 2
    value :DANGER, 3
    value :PROPAGATE, 4
  end
  add_enum "proto.SourceType" do
    value :SOURCE_UNCLASSIFIED, 0
    value :SOURCE_ACCOUNT, 1
    value :SOURCE_BLUETOOTH, 2
    value :SOURCE_BROWSER, 3
    value :SOURCE_CALENDAR, 4
    value :SOURCE_CONTACT, 5
    value :SOURCE_DATABASE, 6
    value :SOURCE_FILE, 7
    value :SOURCE_NETWORK, 8
    value :SOURCE_NFC, 9
    value :SOURCE_SETTINGS, 10
    value :SOURCE_SYNC, 11
    value :SOURCE_UNIQUE_IDENTIFIER, 12
    value :SOURCE_ENVIRONMENT, 51
    value :SOURCE_USER_INPUT, 52
    value :SOURCE_OBFUSCATION, 53
  end
  add_enum "proto.SinkType" do
    value :SINK_UNCLASSIFIED, 0
    value :SINK_ACCOUNT, 1
    value :SINK_AUDIO, 2
    value :SINK_BROWSER, 3
    value :SINK_CALENDAR, 4
    value :SINK_CONTACT, 5
    value :SINK_FILE, 6
    value :SINK_LOG, 7
    value :SINK_NETWORK, 8
    value :SINK_NFC, 9
    value :SINK_PHONE_CONNECTION, 10
    value :SINK_PHONE_STATE, 11
    value :SINK_SMS_MMS, 12
    value :SINK_SYNC, 13
    value :SINK_SYSTEM, 14
    value :SINK_VOIP, 15
    value :SINK_CODE_GENERATION, 51
    value :SINK_PROCESS_OPERATION, 52
    value :SINK_DATABASE, 53
  end
  add_enum "proto.DangerType" do
    value :DANGER_UNCLASSIFIED_DANGER, 0
  end
  add_enum "proto.PropagateType" do
    value :PROPAGATE_UNCLASSIFIED, 0
    value :PROPAGATE_ASSIGN, 1
    value :PROPAGATE_CALL, 2
    value :PROPAGATE_SYSCALL, 3
    value :PROPAGATE_LIBCALL, 4
  end
end

module Proto
  FileInfo = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.FileInfo").msgclass
  SourceLocation = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.SourceLocation").msgclass
  SourceRange = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.SourceRange").msgclass
  AstNode = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.AstNode").msgclass
  AstNode::NodeType = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.AstNode.NodeType").enummodule
  AstLookupConfig = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.AstLookupConfig").msgclass
  PkgAstResult = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.PkgAstResult").msgclass
  PkgAstResults = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.PkgAstResults").msgclass
  Language = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.Language").enummodule
  Functionality = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.Functionality").enummodule
  SourceType = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.SourceType").enummodule
  SinkType = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.SinkType").enummodule
  DangerType = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.DangerType").enummodule
  PropagateType = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.PropagateType").enummodule
end