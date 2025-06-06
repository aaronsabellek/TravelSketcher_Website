import BaseButton from './BaseButton';
import { ButtonProps } from '@/types/models';

// Main Button
const Button: React.FC<ButtonProps> = ({
    text,
    onClick,
    isDisabled,
    type = 'submit',
}) => {
  return (
    <BaseButton
      type={type}
      onClick={onClick}
      isDisabled={isDisabled}
      className="bg-blue-500 text-white hover:bg-blue-600"
    >
      {text}
    </BaseButton>
  );
};

export default Button;