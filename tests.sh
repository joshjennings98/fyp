# tests.sh

rm -f overheadsLog.txt

rm -f gals_100_log.txt
rm -f gals_1000_log.txt 
rm -f gals_10000_log.txt

rm -f clocked_100_log.txt  
rm -f clocked_1000_log.txt 
rm -f clocked_10000_log.txt

rm -f barrier_100_log.txt
rm -f barrier_1000_log.txt
rm -f barrier_10000_log.txt

rm -f extreme_100_log.txt
rm -f extreme_1000_log.txt 
rm -f extreme_10000_log.txt 

rm -f none_100_log.txt 
rm -f none_1000_log.txt
rm -f none_10000_log.txt

echo "GALS sync test\n"

echo "test 1 (GALS, 100, Fully Connected):\n" >> gals_100_log.txt

{ time pts-xmlc gals_100.xml ; } 2>> overheadsLog.txt
{ time pts-serve --headless true >> gals_100_log.txt ; } 2>> gals_100_log.txt

echo "\ntest 2 (GALS, 1000, Fully Connected):\n" >> gals_1000_log.txt

{ time pts-xmlc gals_1000.xml ; } 2>> overheadsLog.txt
{ time pts-serve --headless true >> gals_1000_log.txt ; } 2>> gals_1000_log.txt

echo "\ntest 3 (GALS, 10000, Fully Connected):\n" >> gals_10000_log.txt

#{ time pts-xmlc gals_10000.xml ; } 2>> overheadsLog.txt
#{ time pts-serve --headless true >> gals_10000_log.txt ; } 2>> gals_10000_log.txt

echo "Clocked sync test\n"

echo "\ntest 4 (Clocked, 100, Fully Connected):\n" >> clocked_100_log.txt

{ time pts-xmlc clocked_100.xml ; } 2>> overheadsLog.txt
{ time pts-serve --headless true >> clocked_100_log.txt ; } 2>> clocked_100_log.txt

echo "\ntest 5 (Clocked, 1000, Fully Connected):\n" >> clocked_1000_log.txt

{ time pts-xmlc clocked_1000.xml ; } 2>> overheadsLog.txt
{ time pts-serve --headless true >> clocked_1000_log.txt ; } 2>> clocked_1000_log.txt

echo "\ntest 6 (Clocked, 10000, Fully Connected):\n" >> clocked_10000_log.txt

#{ time pts-xmlc clocked_10000.xml ; } 2>> overheadsLog.txt
#{ time pts-serve --headless true >> clocked_10000_log.txt ; } 2>> clocked_10000_log.txt

echo "Barrier sync test\n"

echo "\ntest 7 (Barrier, 100, Fully Connected):\n" >> barrier_100_log.txt

#{ time pts-xmlc barrier_100.xml ; } 2>> overheadsLog.txt
#{ time pts-serve --headless true >> barrier_100_log.txt ; } 2>> barrier_100_log.txt

echo "\ntest 8 (Barrier, 1000, Fully Connected):\n" >> barrier_1000_log.txt

#{ time pts-xmlc barrier_1000.xml ; } 2>> overheadsLog.txt
#{ time pts-serve --headless true >> barrier_1000_log.txt ; } 2>> barrier_1000_log.txt

echo "\ntest 9 (Barrier, 10000, Fully Connected):\n" >> barrier_10000_log.txt

#{ time pts-xmlc barrier_10000.xml ; } 2>> overheadsLog.txt
#{ time pts-serve --headless true >> barrier_10000_log.txt ; } 2>> barrier_10000_log.txt

echo "Extreme sync test\n"

echo "\ntest 10 (Extreme, 100, Fully Connected):\n" >> extreme_100_log.txt

{ time pts-xmlc extreme_100.xml ; } 2>> overheadsLog.txt
{ time pts-serve --headless true >> extreme_100_log.txt ; } 2>> extreme_100_log.txt

echo "\ntest 11 (Extreme, 1000, Fully Connected):\n" >> extreme_1000_log.txt

{ time pts-xmlc extreme_1000.xml ; } 2>> overheadsLog.txt
{ time pts-serve --headless true >> extreme_1000_log.txt ; } 2>> extreme_1000_log.txt

echo "\ntest 12 (Extreme, 10000, Fully Connected):\n" >> extreme_10000_log.txt

#{ time pts-xmlc extreme_10000.xml ; } 2>> overheadsLog.txt
#{ time pts-serve --headless true >> extreme_10000_log.txt ; } 2>> extreme_10000_log.txt

echo "None sync test\n"

echo "\ntest 13 (None, 100, Fully Connected):\n" >> none_100_log.txt

{ time pts-xmlc none_100.xml ; } 2>> overheadsLog.txt
{ time pts-serve --headless true >> none_100_log.txt ; } 2>> none_100_log.txt

echo "\ntest 14 (None, 1000, Fully Connected):\n" >> none_1000_log.txt

{ time pts-xmlc none_1000.xml ; } 2>> overheadsLog.txt
{ time pts-serve --headless true >> none_1000_log.txt ; } 2>> none_1000_log.txt

echo "\ntest 15 (None, 10000, Fully Connected):\n" >> none_10000_log.txt

#{ time pts-xmlc none_10000.xml ; } 2>> overheadsLog.txt
#{ time pts-serve --headless true >> none_10000_log.txt ; } 2>> none_10000_log.txt
