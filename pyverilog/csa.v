module CSA4 (input [3:0] a, input [3:0] b, input [3:0] c, output [3:0] s, output [3:0] co);

   assign s = a ^ b ^c;
   assign co = a&b | b&c | a&c;

endmodule


