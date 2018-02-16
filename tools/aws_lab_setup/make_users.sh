STUDENTS=30;
echo "users:" > users.yml &&
for NUM in $(seq -f "%02g" 1 $STUDENTS); do
  echo "  - name: Student${NUM}" >> users.yml
  echo "    username: student${NUM}" >> users.yml
  echo "    email: instructor@acme.com" >> users.yml
  echo >> users.yml
done
