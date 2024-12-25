
const badgeColors = ['dark', 'red', 'green', 'yellow', 'indigo', 'purple', 'pink'];

    export function getRandomColor() {
        return badgeColors[Math.floor(Math.random() * badgeColors.length)];
    }