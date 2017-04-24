module CSA4 (
   input [3:0] a,b,c,
   output [3:0] s, co);

   assign s = a ^ b ^c;
   assign co = a&b | b&c | a&c;
endmodule


