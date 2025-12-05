if ARGV.length != 3
  STDERR.puts "Maaf, ada sedikit kesalahan"
  exit 2
end

op = ARGV[0]
begin
  a = Float(ARGV[1])
  b = Float(ARGV[2])
rescue => e
  STDERR.puts "Invalid number"
  exit 3
end

result = nil
case op
when '+'
  result = a + b
when '-'
  result = a - b
when 'x'
  result = a * b
when '^'
  result = a ** b
when '%'
  result = a % b
when '/'
  if b == 0.0
    STDERR.puts "Nah!"
    exit 4
  end
  result = a / b
else
  STDERR.puts "Not Supported"
  exit 5
end

# Hapus trailing zeros jika merupakan bilangan bulat
if result == result.to_i
  puts result.to_i
else
  puts result
end
