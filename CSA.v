module CSA4 (input [3:0] a, input [3:0] b, input [3:0] c, output [3:0] s, output [3:0] co);
// module CSA4 (
//     input logic [3:0] a,b,c,
//     output logic[3:0] s, co);

   assign s = a ^ b ^c;
   assign co = a&b | b&c | a&c;

// endmodule

endmodule

module main (input [3:0] a, input [3:0] b, input [3:0] c, output [3:0] s, output [3:0] co);
wire [3:0] inst0_s;
wire [3:0] inst0_co;
CSA4 inst0 (.a(a), .b(b), .c(c), .s(inst0_s), .co(inst0_co));
assign s = inst0_s;
assign co = inst0_co;
endmodule

